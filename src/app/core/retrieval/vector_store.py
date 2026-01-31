"""Vector store wrapper for ChromaDB integration with LangChain."""

from pathlib import Path
from functools import lru_cache
from typing import List

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


from ..config import get_settings


@lru_cache(maxsize=1)
def _get_vector_store() -> Chroma:
    """Create a Chroma vector store instance configured from settings."""
    settings = get_settings()

    embeddings = OpenAIEmbeddings(
        model=settings.openai_embedding_model_name,
        api_key=settings.openai_api_key,
    )

    return Chroma(
        collection_name="rag-collection",
        embedding_function=embeddings,
        persist_directory=settings.chroma_persist_directory,
    )

def get_retriever(k: int | None = None):
    """Get a Chroma retriever instance.

    Args:
        k: Number of documents to retrieve (defaults to config value).

    Returns:
        Chroma vector store retriever.
    """
    settings = get_settings()
    if k is None:
        k = settings.retrieval_k

    vector_store = _get_vector_store()
    return vector_store.as_retriever(search_kwargs={"k": k})


def retrieve(query: str, k: int | None = None) -> List[Document]:
    """Retrieve documents from Chroma for a given query.

    Args:
        query: Search query string.
        k: Number of documents to retrieve (defaults to config value).

    Returns:
        List of Document objects with metadata (including page numbers).
    """
    retriever = get_retriever(k=k)
    return retriever.invoke(query)

def index_documents(file_path: Path) -> int:
    """Index a list of Document objects into the Chroma vector store.

    Args:
        file_path: Path to the PDF file to index.

    Returns:
        The number of documents indexed.
    """
    loader = PyPDFLoader(str(file_path))
    # Load all pages
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(docs)

    vector_store = _get_vector_store()
    vector_store.add_documents(texts)
    
    return len(texts)