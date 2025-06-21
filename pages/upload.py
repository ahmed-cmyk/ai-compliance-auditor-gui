import os
import streamlit as st

from pipelines.ingestion import PDFLoader, TextSplitter
from services.vector_store import VectorManager

def save_files(uploaded_files):
    data_dir = "data/uploaded_docs"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    pdf_loader = PDFLoader()
    text_splitter = TextSplitter().get_text_splitter()

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_path = os.path.join(data_dir, file_name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        chunks = pdf_loader.load_and_split(file_path, text_splitter)

        save_to_vector_store(chunks)

def save_to_vector_store(chunks):
    vector_manager = VectorManager()
    vector_store = vector_manager.get_vector_store()

    vector_store.add_documents(chunks)

st.title("Document Upload")

st.markdown("""
Upload your documents for analysis. Supported formats: PDF, DOCX, and TXT files.
""")

with st.form("upload_form", clear_on_submit=True):
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="You can select multiple files at once"
    )
    save_button = st.form_submit_button("Save", use_container_width=True, type="primary")

    if save_button:
        if not uploaded_files:
            st.warning("Please upload at least one file before saving.")
        else:
            save_files(uploaded_files)
