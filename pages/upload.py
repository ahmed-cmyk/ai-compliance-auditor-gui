import os
import streamlit as st
from typing import List
from langchain_core.documents import Document

from pipelines.ingestion import PDFLoader, TextSplitter
from services.vector_store import VectorManager

def save_files(uploaded_files):
    data_dir = "data/uploaded_docs"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    pdf_loader = PDFLoader()
    text_splitter = TextSplitter().get_text_splitter()
    
    # Initialize progress tracking
    total_files = len(uploaded_files)
    processed_files = 0
    total_chunks = 0
    
    # Progress bar for overall file processing
    overall_progress = st.progress(0, text="Processing files...")
    status_text = st.empty()
    
    all_chunks = []
    
    # Process each file with progress indication
    for i, uploaded_file in enumerate(uploaded_files):
        file_name = uploaded_file.name
        file_path = os.path.join(data_dir, file_name)
        
        # Update status
        status_text.text(f"Processing {file_name}...")
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Load and split document with progress indication
        with st.spinner(f"Loading and chunking {file_name}..."):
            chunks = pdf_loader.load_and_split(file_path, text_splitter)
            all_chunks.extend(chunks)
            total_chunks += len(chunks)
        
        processed_files += 1
        overall_progress.progress(processed_files / total_files, text=f"Processed {processed_files}/{total_files} files")
    
    # Clear status text
    status_text.empty()
    
    # Save to vector store with progress indication
    if all_chunks:
        save_to_vector_store(all_chunks, total_chunks)
    
    overall_progress.empty()
    st.success(f"Successfully processed {total_files} files with {total_chunks} total chunks!")

def save_to_vector_store(chunks: List[Document], total_chunks: int):
    """Save chunks to vector store with progress indication"""
    vector_manager = VectorManager()
    vector_store = vector_manager.get_vector_store()
    
    # Progress bar for vector storage
    storage_progress = st.progress(0, text="Storing documents in vector database...")
    storage_status = st.empty()
    
    # Process in batches for better performance and progress tracking
    batch_size = 100
    total_batches = (total_chunks + batch_size - 1) // batch_size
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_chunks)
        batch_chunks = chunks[start_idx:end_idx]
        
        # Update status
        storage_status.text(f"Storing batch {batch_num + 1}/{total_batches} ({len(batch_chunks)} chunks)...")
        
        # Add documents to vector store
        vector_store.add_documents(batch_chunks)
        
        # Update progress
        progress = (batch_num + 1) / total_batches
        storage_progress.progress(progress, text=f"Stored {end_idx}/{total_chunks} chunks")
    
    # Clear progress indicators
    storage_progress.empty()
    storage_status.empty()

st.title("Document Upload")

st.markdown("""
Upload your documents for analysis. Supported formats: PDF, DOCX, and TXT files.

**Note:** Large files may take some time to process. You'll see progress indicators during the upload and processing.
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
            # Show file count and estimated processing info
            st.info(f"Processing {len(uploaded_files)} file(s)...")
            save_files(uploaded_files)
