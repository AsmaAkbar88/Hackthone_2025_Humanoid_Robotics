import requests
import json
from datetime import datetime

# Define the API endpoint
BASE_URL = "http://localhost:8000/api"

def create_new_account(email, password, name=None, date_of_birth=None):
    """
    Create a new user account in the Neon database
    """
    url = f"{BASE_URL}/auth/signup"
    
    payload = {
        "email": email,
        "password": password,
        "name": name,
        "date_of_birth": date_of_birth,
        "signup_date": datetime.utcnow().isoformat()
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("Account created successfully!")
            print(f"User ID: {result['data']['user']['id']}")
            print(f"Email: {result['data']['user']['email']}")
            print(f"Name: {result['data']['user'].get('name', 'N/A')}")
            print(f"Access Token: {result['data']['access_token'][:20]}...")  # Truncate token for display
            return result
        else:
            print(f"Failed to create account. Status code: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the backend server. Please make sure it's running on http://localhost:8000")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage - create a new account with predefined values
    print("Creating a new account in the Neon database...")
    
    # Predefined values for the new account
    new_email = "testuser@example.com"
    new_password = "securepassword123"
    new_name = "Test User"
    dob_input = "1990-01-01"  # Optional: date of birth in YYYY-MM-DD format
    
    result = create_new_account(
        email=new_email,
        password=new_password,
        name=new_name,
        date_of_birth=dob_input
    )
    
    if result:
        print("\nAccount creation completed successfully!")
        print("Note: The account has been saved directly to the Neon database.")
    else:
        print("\nAccount creation failed!")