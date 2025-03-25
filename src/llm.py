import streamlit as st
import os


from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.core.chat_engine.types import ChatMode
import genius

llm = None
embedding = None

from dotenv import load_dotenv
load_dotenv()
VLLM_ENDPOINT = os.getenv("VLLM_ENDPOINT")
VLLM_TOKEN = os.getenv("VLLM_TOKEN")
VLLM_MODEL = os.getenv("VLLM_MODEL")
if VLLM_ENDPOINT is None or VLLM_TOKEN is None:
    MODEL_NAME = os.getenv("MODEL_NAME") or "llama3.2"

    from llama_index.llms.ollama import Ollama
    from llama_index.embeddings.ollama import OllamaEmbedding
    llm = Ollama(model=MODEL_NAME, request_timeout=120)
    embedding = OllamaEmbedding(model_name=MODEL_NAME)
else:
    from llama_index.llms.openai_like import OpenAILike
    import httpx
    httpx_client = httpx.Client(verify=False)
    llm = OpenAILike(
        model=VLLM_MODEL,
        api_base=VLLM_ENDPOINT,
        api_key=VLLM_TOKEN,
        api_version="v1",
        http_client=httpx_client,
        max_tokens=1024,
    )


@st.cache_resource(show_spinner=False)
def load_llm(artist, tmpdirname):
    with st.spinner(text="Loading model"):
        Settings.llm = llm
        Settings.embed_model = embedding
    docs = []
    song_names = genius.get_artist_songs(artist)
    genius.write_lyrics(song_names, artist, tmpdirname)
    with st.spinner(text=f"Loading {artist} lyrics in LLM", show_time=True):
        reader = SimpleDirectoryReader(input_dir=tmpdirname, recursive=True)
        docs = reader.load_data()
    with st.spinner(text=f"Indexing {len(docs)} songs"):
        index = VectorStoreIndex.from_documents(docs)
        return index.as_chat_engine(ChatMode.CONTEXT)
