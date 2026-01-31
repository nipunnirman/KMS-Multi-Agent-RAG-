
import sys
import requests
from pathlib import Path

# Add src to path
sys.path.append(str(Path.cwd() / "src"))

from dotenv import load_dotenv
load_dotenv()

def check_system():
    print("🏥 Starting System Health Check...\n")
    
    # 1. Check Pinecone Connection
    try:
        print("🌲 Checking Pinecone Configuration...")
        from app.core.retrieval.vector_store import _get_vector_store, get_settings
        settings = get_settings()
        
        print(f"   - API Key present: {bool(settings.pinecone_api_key)}")
        print(f"   - Index Name: {settings.pinecone_index_name}")
        print(f"   - Host: {settings.pinecone_host or 'Auto-resolve'}")
        
        vs = _get_vector_store()
        # Try a lightweight operation to verify connection
        # We can't easily ping without an index check, but initialization is a good first step
        print("   ✅ Pinecone VectorStore initialized successfully.")
    except Exception as e:
        print(f"   ❌ Pinecone Error: {e}")

    # 2. Check Running API
    print("\n🔌 Checking API Endpoint (http://127.0.0.1:8000)...")
    try:
        payload = {"question": "Test query"}
        response = requests.post("http://127.0.0.1:8000/qa", json=payload)
        
        print(f"   - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ API is working and returned an answer.")
        elif response.status_code == 500:
            print("   ⚠️ API Error (500). Detailed error below implies cause (likely OpenAI quota):")
            print(f"   {response.text[:200]}...") # Print first 200 chars
        else:
            print(f"   ⚠️ Unexpected Status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to API. Is 'uvicorn' running?")
    except Exception as e:
        print(f"   ❌ API Check Failed: {e}")

if __name__ == "__main__":
    check_system()
