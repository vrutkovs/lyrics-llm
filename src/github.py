import streamlit as st

prompt_template = '''
Create a poem about a request for review of pull request {pull_request_url}.
This is a PR for {github_pr.organization} organization in {github_pr.repository} repository.
Title of the PR is "{github_pr.title}". The poem must end with the URL and be no longer than 4 lines.
'''

class GithubPullRequestInfo:
    title = "Issue short lived certificates if ShortCertRotation featuregate is enabled"
    organization = "openshift"
    repository = "cluster-kube-apiserver-operator"

    def __init__(self, url):
        self.url = url
        # TODO: Fetch pull request details here

@st.cache_data
def fetch_pull_request_info(url):
    # TODO: Validate URL
    return GithubPullRequestInfo(url)


@st.cache_data
def get_prompt(url):
    github_pr = fetch_pull_request_info(url)
    return prompt_template.format(
        pull_request_url=url,
        github_pr=github_pr,
    )
