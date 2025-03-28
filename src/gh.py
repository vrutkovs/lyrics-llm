import os
import streamlit as st
from github import Github, Auth
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_ACCESS_TOKEN")
if token is None:
    raise ValueError("GITHUB_ACCESS_TOKEN environment variable is not set")
g = Github(auth=Auth.Token(token))

class GithubPullRequestInfo:
    title = ""
    organization = ""
    repository = ""
    ticket_url = ""
    pull_request_url = ""

    def __init__(self, url):
        o = urlparse(url)
        if o.netloc != "github.com":
            raise ValueError("Invalid URL")

        repository, pull_request_id = self.split_path(o.path)
        repo = g.get_repo(repository)
        self.organization = repo.organization.name
        self.repository = repo.name

        pr = repo.get_pull(int(pull_request_id))
        self.set_title_and_ticket_url(pr.title)
        self.pull_request_url = pr.html_url

    def split_path(self, path):
        remainder, pull_request_id = os.path.split(path)
        if len(remainder) == 0:
            raise ValueError("Unable to find pull request ID")
        remainder, issues_or_pullrequest = os.path.split(remainder)
        if len(remainder) == 0:
            raise ValueError("Unable to find issues/pulls part")
        return remainder.strip("/"), pull_request_id

    def set_title_and_ticket_url(self, title):
        # TODO: Implement title sanitization logic
        if ":" not in title:
            self.title = title.strip()
            return
        ticket_id, remainder = title.split(sep=":", maxsplit=1)
        if len(ticket_id) != 0 and ticket_id not in ["NO-JIRA", "NO-ISSUE"]:
            # Set JIRA ticket URL
            self.ticket_url = f"https://issues.redhat.com/browse/{ticket_id}"
        self.title = remainder.strip()


@st.cache_data(show_spinner=False)
def fetch_pull_request_info(url):
    # TODO: Validate URL
    return GithubPullRequestInfo(url)
