import streamlit as st
import os

from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.core.chat_engine.types import ChatMode

# TODO: Import if vLLM env var not set
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

import genius
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME")
if MODEL_NAME is None:
    MODEL_NAME = "llama3.2"


@st.cache_resource(show_spinner=False)
def load_llm(artist, tmpdirname):
    with st.spinner(text="Loading model"):
        Settings.llm = Ollama(model=MODEL_NAME, request_timeout=120)
        Settings.embed_model = OllamaEmbedding(model_name=MODEL_NAME)
    docs = []
    song_names = genius.get_artist_songs(artist)
    with st.spinner(text=f"Fetching {artist} lyrics"):
        genius.write_lyrics(song_names, artist, tmpdirname)
    with st.spinner(text=f"Loading {artist} lyrics in LLM"):
        reader = SimpleDirectoryReader(input_dir=tmpdirname, recursive=True)
        docs = reader.load_data()
    with st.spinner(text=f"Indexing {len(docs)} songs"):
        index = VectorStoreIndex.from_documents(docs)
        return index.as_chat_engine(ChatMode.CONTEXT)
