
import os
import sys
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent / "src"))

from app.core.config import get_settings
from app.core.llm.factory import create_chat_model
from langchain_core.messages import HumanMessage

def main():
    try:
        settings = get_settings()
        print(f"Loaded Key: {settings.openai_api_key[:10]}...{settings.openai_api_key[-5:]}")
        
        print("Creating ChatModel...")
        chat = create_chat_model()
        
        print("Invoking ChatModel...")
        response = chat.invoke([HumanMessage(content="Hello")])
        print("Success!")
        print(response.content)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
