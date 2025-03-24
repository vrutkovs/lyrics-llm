import streamlit as st
import os

from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.genius import GeniusReader
from llama_index.core.chat_engine.types import ChatMode

# TODO: Import if vLLM env var not set
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GENIUS_ACCESS_TOKEN")
if token is None:
    raise ValueError("GENIUS_ACCESS_TOKEN environment variable is not set")

@st.cache_resource(show_spinner=False)
def load_llm(artist):
    with st.spinner(text="Loading model"):
        Settings.llm = Ollama(model="llama3.2", request_timeout=120)
    with st.spinner(text="Loading embeddings"):
        Settings.embed_model = OllamaEmbedding(model_name="llama3.2")
    with st.spinner(text=f"Looking up artist {artist} on Genius"):
        reader = GeniusReader(token)
        docs = reader.load_artist_songs(artist_name=artist, max_songs=50)
        st.write(f"Found {docs}")
    with st.spinner(text=f"Indexing {len(docs)} songs"):
        index = VectorStoreIndex.from_documents(docs)
        return index.as_chat_engine(ChatMode.CONTEXT)
