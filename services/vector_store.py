from .embeddings import embeddings
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="compliance_auditor_collection",
    embedding_function=embeddings,
    persist_directory="../data/chromadb",
)

