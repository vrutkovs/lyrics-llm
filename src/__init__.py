from llama_index.core.chat_engine.types import ChatMode
import random
import streamlit as st
import llm
import gh

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Start with pasting a github pull request link here"}
    ]
is_first_message = len(st.session_state.messages) == 1

st.header("PTAL Generator")
prompt = ""
index = llm.load_llm()
chat_engine = index.as_chat_engine(ChatMode.CONDENSE_PLUS_CONTEXT)

if user_input := st.chat_input(key="user_input", placeholder="Send message"):
    if is_first_message:
        with st.spinner("Fetching github pull request details"):
            prompt = gh.get_prompt(user_input)
    else:
        prompt = str(user_input)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

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

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner(get_spinner_text()):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
