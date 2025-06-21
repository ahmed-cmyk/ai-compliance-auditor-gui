from langchain_chroma import Chroma
from langchain_chroma.vectorstores import Chroma
from typing import Optional

from .embeddings import EmbeddingService

class VectorManager:
    def __init__(self):
        self.vector_store: Optional[Chroma] = None

    def get_vector_store(self) -> Chroma:
        if not self.vector_store:
            embeddings = EmbeddingService().get_embedding_model()

            self.vector_store = Chroma(
                collection_name="compliance_auditor_collection",
                embedding_function=embeddings,
                persist_directory="../data/chromadb",
            )

        return self.vector_store

