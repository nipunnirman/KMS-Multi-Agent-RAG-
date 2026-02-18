
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"Testing API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")

try:
    client = OpenAI(api_key=api_key)
    
    print("Testing Models List...")
    models = client.models.list()
    print(f"Models List Success. Found {len(models.data)} models.")
    
    print("Test 1: Simple User Message (Default Temp)")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print("Test 1 Success")
    except Exception as e:
        print(f"Test 1 Failed: {e}")

    print("\nTest 2: User Message + Temp 0.0")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.0,
            max_tokens=5
        )
        print("Test 2 Success")
    except Exception as e:
        print(f"Test 2 Failed: {e}")

    print("\nTest 3: System + User Message (Default Temp)")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello"}
            ],
            max_tokens=5
        )
        print("Test 3 Success")
    except Exception as e:
        print(f"Test 3 Failed: {e}")
        
    print("\nTest 4: System + User Message + Temp 0.0")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello"}
            ],
            temperature=0.0,
            max_tokens=5
        )
        print("Test 4 Success")
    except Exception as e:
        print(f"Test 4 Failed: {e}")
except Exception as e:
    print(f"Error: {e}")
