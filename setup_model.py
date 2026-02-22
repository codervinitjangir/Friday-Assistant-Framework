import requests
import json
import sys

def pull_model():
    url = "http://localhost:11434/api/pull"
    payload = {
        "model": "qwen2.5:3b",
        "stream": False
    }
    
    print("Starting download of qwen2.5:3b via API...")
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        # Stream response to show progress (though stream=False above waits for completion)
        # Verify if successful
        if response.status_code == 200:
            print("Successfully requested model pull!")
            print(response.json())
        else:
            print(f"Failed: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Ollama is running! (Step 1: ollama serve)")

if __name__ == "__main__":
    pull_model()
