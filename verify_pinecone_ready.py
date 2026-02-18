import os
import sys
from pathlib import Path

# Add src to python path to import config
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from app.core.config import get_settings
    from pinecone import Pinecone
    
    settings = get_settings()
    print(f"Checking Pinecone configuration...")
    print(f"Index name: {settings.pinecone_index_name}")
    print(f"Host: {settings.pinecone_host}")
    
    pc = Pinecone(api_key=settings.pinecone_api_key)
    
    # Check if index exists
    indexes = pc.list_indexes()
    print(f"Available indexes: {[i.name for i in indexes]}")
    
    if settings.pinecone_index_name not in [i.name for i in indexes]:
        print(f"ERROR: Index '{settings.pinecone_index_name}' not found!")
        sys.exit(1)
        
    index = pc.Index(settings.pinecone_index_name)
    stats = index.describe_index_stats()
    print(f"Index stats: {stats}")
    print("Pinecone connection successful!")
    
except Exception as e:
    print(f"Error verifying Pinecone: {e}")
    sys.exit(1)
