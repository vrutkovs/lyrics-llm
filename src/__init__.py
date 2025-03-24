import random
import streamlit as st
import llm
import gh

prompt_template = '''
Create a poem in the style of {artist} about a request for review of pull request.
This is a PR for {github_pr.organization} organization in {github_pr.repository} repository.
Title of the PR is "{github_pr.title}".

The poem must not exceed 4 lines. Each line should have a maximum of 10 words. Each line should start with a capital letter and end with a period.
Each line should be separated by double line break. Poem should be creative and engaging.

The poem must end with links to {pull_request_url} and {github_pr.ticket_url}
'''

@st.cache_data(show_spinner=False)
def get_prompt(url, artist):
    github_pr = gh.fetch_pull_request_info(url)
    return prompt_template.format(
        pull_request_url=url,
        github_pr=github_pr,
        artist=artist
    )

def get_spinner_text():
    spinner_texts = [
        "Thinking...",
        "Asking the spirit of Homer...",
        "Consulting with Shakespeare...",
        "John Keats is advising...",
        "Emily Dickinson is preparing an answer...",
        "T.S. Eliot is pondering..."
    ]
    return random.choice(spinner_texts)

st.session_state.is_initialized = "messages" in st.session_state.keys()

st.header("PTAL Generator")
chat_engine = llm.load_llm()

if not st.session_state.is_initialized:
    with st.form("input_form"):
        pull_request_url = st.text_input("Github PR link")
        artist = st.text_input("Music artist")
        submitted = st.form_submit_button("Submit")
        if submitted and len(pull_request_url) > 0 and len(artist) > 0:
            st.session_state.pull_request_url = pull_request_url
            st.session_state.artist = artist
            st.session_state.is_initialized = True
            st.session_state.poem_generated = False
            st.session_state.messages = []

if st.session_state.is_initialized:
    if not st.session_state.poem_generated:
        with st.spinner("Fetching github pull request details"):
            prompt = get_prompt(
                url=st.session_state.pull_request_url,
                artist=st.session_state.artist)
            st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.poem_generated = True

    if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages: # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    last_message = st.session_state.messages[-1]
    if last_message["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner(get_spinner_text()):
                response = chat_engine.chat(last_message["content"])
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message) # Add response to message history
