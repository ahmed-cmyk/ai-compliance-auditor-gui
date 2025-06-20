from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
        Field,
)

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    project_name: str = Field('AI Compliance Auditor')

    embedding_model_name: str = Field('llama3.1:8b')

    default_chunk_size: int = 1000
    default_chunk_overlap: int = 200
    ollama_base_url: str = Field("http://localhost:11434", description="Base URL for the Ollama server API")


settings = AppConfig()
