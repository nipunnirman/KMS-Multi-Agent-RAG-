import sys
import asyncio
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from app.services.qa_service import answer_question
    from app.core.config import get_settings
    
    print("Settings loaded successfully.")
    settings = get_settings()
    print(f"Pinecone Index: {settings.pinecone_index_name}")
    
    question = "What is the net income reported?"
    print(f"\nAttempting to answer question: '{question}'")
    
    result = answer_question(question)
    
    print("\nSUCCESS!")
    print(f"Answer: {result.get('answer', 'No answer key provided')}")
    print(f"Context documents: {len(result.get('context', []))} retrieved")
    
except Exception as e:
    print(f"\nFAILURE: {e}")
    import traceback
    traceback.print_exc()
