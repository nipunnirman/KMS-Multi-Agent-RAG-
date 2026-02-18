import sys
import time
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from app.core.config import get_settings
    from pinecone import Pinecone, ServerlessSpec
    
    settings = get_settings()
    pc = Pinecone(api_key=settings.pinecone_api_key)
    
    index_name = settings.pinecone_index_name
    
    # Check if index exists
    existing_indexes = [i.name for i in pc.list_indexes()]
    
    if index_name in existing_indexes:
        print(f"Index '{index_name}' already exists.")
    else:
        print(f"Creating index '{index_name}'...")
        # Create serverless index in us-east-1
        pc.create_index(
            name=index_name,
            dimension=3072, # text-embedding-3-large
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"Index '{index_name}' creation initiated.")
        
        # Wait for index to be ready
        while not pc.describe_index(index_name).status['ready']:
            print("Waiting for index to be ready...")
            time.sleep(1)
            
        print(f"Index '{index_name}' is ready!")
        
    # Print host for .env verification
    index_description = pc.describe_index(index_name)
    print(f"Index Host: {index_description.host}")
    
except Exception as e:
    print(f"Error creating index: {e}")
    sys.exit(1)
