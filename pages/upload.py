import streamlit as st

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