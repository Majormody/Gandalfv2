from indexing.embedder import Embedder
from pipeline import RagPipeline
from data_schemas import GenerationResult


import streamlit as st




@st.cache_resource
def get_embedder()-> Embedder:
    return Embedder()



def get_pipeline()-> RagPipeline:
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = RagPipeline(get_embedder())
    return st.session_state.pipeline


def get_chat_history()-> list[tuple[str, GenerationResult]]:
    st.session_state.setdefault("chat_history", [])
    return st.session_state.chat_history


def append_to_chat_history(query: str, result: GenerationResult)-> None:
    chat_history = get_chat_history()
    chat_history.append((query, result))
        