from data_schemas import GenerationResult


import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def render_upload_widget()-> UploadedFile | None:
    """Renders the upload widget, Returns the uploaded File"""
    datasheet = st.file_uploader(label="Upload Your Datasheet", type="pdf")
    return datasheet

def render_answer(result: GenerationResult)-> None:
    """Renders the answer, its similarity score and the sources"""
    st.write(result.answer)

    with st.expander("Text Sources"):
        for text_source in result.sources.text_chunks:
            st.write(text_source.chunk.content)
            st.write(f"Match Strength: {text_source.score:.2f}")
            if text_source.chunk.page_number:
                st.write(f"Page Number: {text_source.chunk.page_number}")
            st.write(f"Path: H1: {text_source.chunk.metadata.get('h1')} H2: {text_source.chunk.metadata.get('h2')}")

    with st.expander("Table Sources"):
        for table_source in result.sources.table_chunks:
            st.write(table_source.chunk.content)
            st.write(f"Match Strength: {table_source.score:.2f}")
            if table_source.chunk.page_number:
                st.write(f"Page Number: {table_source.chunk.page_number}")
            

def render_chat_history(history: list[tuple[str, GenerationResult]])-> None:
    """Renders the chat history"""
    for question, result in history:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            render_answer(result)