from langchain_ollama import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from typing import Optional

from config.settings import settings


class EmbeddingService:
    """
    Manages the initialization and access to the chosen embedding model.
    Pulls configuration from AppConfig.
    """
    def __init__(self):
        self._embedding_model: Optional[Embeddings] = None

    def get_embedding_model(self) -> Embeddings:
        """
        Initializes and returns the configured embedding model.
        """
        if self._embedding_model is None:
            model_name = settings.embedding_model_name
            try:
                self._embedding_model = OllamaEmbeddings(
                    model=model_name,
                    base_url=settings.ollama_base_url # Assuming you add this to AppConfig
                )
            except Exception as e:
                raise RuntimeError(f"Embedding service initialization failed: {e}") from e

        return self._embedding_model
