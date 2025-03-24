import streamlit as st

from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader

# TODO: Import if vLLM env var not set
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

@st.cache_resource(show_spinner=False)
def load_llm():
    Settings.llm = Ollama(model="llama3.2", request_timeout=120)
    Settings.embed_model = OllamaEmbedding(model_name="llama3.2")
    with st.spinner(text="Loading and indexing lyrics"):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        index = VectorStoreIndex.from_documents(docs)
        return index
