import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_create_profile():
    """Test the create-profile endpoint"""
    endpoint = f"{BASE_URL}/create-profile"
    
    # Test data
    data = {
        "risk_tolerance": "moderate",
        "investment_timeline": "5-10 years",
        "financial_goals": ["Retirement", "Children's Education"],
        "initial_investment": 1000000
    }
    
    # Make POST request
    try:
        response = requests.post(endpoint, json=data)
        print("\n=== Create Profile Test ===")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

def test_generate_portfolio():
    """Test the generate-portfolio endpoint"""
    endpoint = f"{BASE_URL}/generate-portfolio"
    
    # Test data
    data = {
        "risk_tolerance": "moderate",
        "investment_timeline": "5-10 years",
        "financial_goals": ["Retirement", "Children's Education"],
        "initial_investment": 1000000
    }
    
    # Make POST request
    try:
        response = requests.post(endpoint, json=data)
        print("\n=== Generate Portfolio Test ===")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Test both endpoints
    test_create_profile()
    test_generate_portfolio()
