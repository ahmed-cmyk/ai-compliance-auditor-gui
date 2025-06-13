import streamlit as st
from langchain_ollama.chat_models import ChatOllama

chat_page = st.Page("pages/chat.py", title="Chat", icon=":material/chat:")
upload_page = st.Page("pages/upload.py", title="Upload", icon=":material/upload_file:")
settings_page = st.Page("pages/settings.py", title="Settings", icon=":material/settings:")

pg = st.navigation([chat_page, upload_page, settings_page])

if __name__ == "__main__":
    pg.run()
