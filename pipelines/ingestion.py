from abc import ABC, abstractmethod
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from typing import List
from config.settings import settings

"""
Loader classes that handle loading data from a document and then splitting that data into chunks
and returning it.

The loaders currently only support PDFs and web pages.
"""
class BaseDocumentLoader(ABC):
    @abstractmethod
    def load_and_split(self, source_identifier: str, text_splitter: RecursiveCharacterTextSplitter) -> List[Document]:
        """
        Abstract method to load raw content from a source and split it into Langchain Documents.
        
        Args:
            source_identifier: The path (file path, URL, etc.) to the document.
            text_splitter: An instance of RecursiveCharacterTextSplitter to use.
            
        Returns:
            A list of Langchain Document objects.
        """
        pass


class PDFLoader(BaseDocumentLoader):
    def load_and_split(self, source_identifier: str, text_splitter: RecursiveCharacterTextSplitter) -> List[Document]:
        source_path = source_identifier

        if not source_identifier or not os.path.exists(source_path):
            print("File Not Found")
            return []

        loader = PyPDFLoader(source_identifier)
        return loader.load_and_split(text_splitter)


class WebLoader(BaseDocumentLoader):
    def load_and_split(self, source_identifier: str, text_splitter: RecursiveCharacterTextSplitter) -> List[Document]:
        page_url = source_identifier

        loader = WebBaseLoader(web_paths=[page_url])
        return loader.load_and_split(text_splitter)


"""
Returns a text splitter object with the specified configuration settings.
"""
class TextSplitter:
    @staticmethod
    def get_text_splitter(
        chunk_size: int = settings.default_chunk_size,
        chunk_overlap: int = settings.default_chunk_overlap
    ):
        """Returns a configured RecursiveCharacterTextSplitter"""
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
