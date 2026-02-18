import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    print("Testing /api/analyze...")
    try:
        response = requests.post(f"{base_url}/api/analyze", json={"query": "What is gradient descent?"})
        if response.status_code == 200:
            print("Analyze Success:", response.json())
        else:
            print("Analyze Failed:", response.status_code, response.text)
    except Exception as e:
        print("Analyze Error:", e)

if __name__ == "__main__":
    test_api()
