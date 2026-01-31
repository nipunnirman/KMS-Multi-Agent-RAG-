
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path.cwd() / "src"))

from dotenv import load_dotenv
load_dotenv()

try:
    print("🔍 Testing Pinecone Retrieval directly...")
    from app.core.retrieval.vector_store import retrieve

    query = "net income"
    print(f"❓ Querying for: '{query}'")
    
    docs = retrieve(query, k=2)
    
    print(f"\n✅ Successfully retrieved {len(docs)} documents from Pinecone.")
    for i, doc in enumerate(docs):
        print(f"\n--- Document {i+1} ---")
        content_preview = doc.page_content[:150].replace('\n', ' ')
        print(f"Content: {content_preview}...")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        
except Exception as e:
    print(f"\n❌ Retrieval Failed: {e}")
