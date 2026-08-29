from ui.components import render_chat_history, render_answer, render_upload_widget
from ui.state import get_pipeline, get_chat_history, append_to_chat_history, get_embedder


import streamlit as st


st.set_page_config(
    page_title="Gandalf",
    page_icon="🧙",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Datasheet RAG")

with st.sidebar:
    st.header("Document")
    datasheet = render_upload_widget()

    num_of_text_chunks = st.slider(
        label = "Content sections to retrieve",
        min_value = 3,
        max_value= 10
    )

    num_of_table_chunks = st.slider(
            label = "Structured tables to retrieve",
            min_value = 8,
            max_value= 12
        )

    process_button = st.button(
        "Process document",
        type="primary",
        use_container_width=True,
    )

    if datasheet and process_button:
        with st.spinner("Processing document..."):
            get_pipeline().ingest(
                datasheet.getvalue(),
                datasheet.name,
                status_fn=st.write,
            )
        st.success("Ready!")

query = st.chat_input("Ask about the datasheet")

if query:
    result = get_pipeline().ask(query, n_text=num_of_text_chunks, n_table=num_of_table_chunks)
    append_to_chat_history(query, result)

render_chat_history(get_chat_history())
