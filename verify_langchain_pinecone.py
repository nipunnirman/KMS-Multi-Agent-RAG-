
import sys
import os
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
load_dotenv()

try:
    from app.core.config import get_settings
    from pinecone import Pinecone
    from langchain_pinecone import PineconeVectorStore
    from langchain_openai import OpenAIEmbeddings

    settings = get_settings()
    print(f"API Key: {settings.pinecone_api_key[:5]}...")
    print(f"Index: {settings.pinecone_index_name}")
    print(f"Host: {settings.pinecone_host}")
    
    pc = Pinecone(api_key=settings.pinecone_api_key)
    # index = pc.Index(settings.pinecone_index_name, host=settings.pinecone_host)
    print("Initializing Index without explicit host...")
    index = pc.Index(settings.pinecone_index_name)
    
    embeddings = OpenAIEmbeddings(
        model=settings.openai_embedding_model_name,
        api_key=settings.openai_api_key,
    )
    
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
    )
    
    print("Attempting similarity search...")
    docs = vector_store.similarity_search("test", k=1)
    print(f"Found {len(docs)} documents.")
    print("Success!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
