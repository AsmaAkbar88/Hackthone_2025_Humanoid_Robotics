import requests
import json

# Test the backend API
BASE_URL = "http://localhost:8000/api"

def test_api_connection():
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"API Root Response: {response.status_code}")
        print(f"API Root Content: {response.text[:200]}...")
        return True
    except requests.exceptions.RequestException as e:
        print(f"API Connection Error: {e}")
        return False

def test_login():
    try:
        # Test login with dummy credentials
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        print(f"Login Response Status: {response.status_code}")
        print(f"Login Response: {response.text[:500]}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Login Request Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing API connection...")
    if test_api_connection():
        print("\nTesting login functionality...")
        test_login()
    else:
        print("\nCould not connect to API. Please ensure the backend server is running.")