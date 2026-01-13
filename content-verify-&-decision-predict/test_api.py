import requests
import json
import sys

# URL of the FastAPI application
url = "http://127.0.0.1:8000/analyze"

# Test cases
test_cases = [
    {
        "name": "Valid Professional Post",
        "payload": {
            "User_Text": "Our new AI model increases diagnostic accuracy by 15% for early-stage detection.",
            "Registered_Domain": "Healthcare"
        }
    },
    {
        "name": "Off-topic / Unprofessional",
        "payload": {
            "User_Text": "I can't believe the game last night! Referees were blind.",
            "Registered_Domain": "Healthcare"
        }
    },
    {
        "name": "Domain Mismatch",
        "payload": {
            "User_Text": "Check out this new real estate investment opportunity downtown.",
            "Registered_Domain": "EdTech"
        }
    }
]

print(f"Testing API at {url}...\n")

for test in test_cases:
    print(f"--- Running Test: {test['name']} ---")
    print(f"Input: {json.dumps(test['payload'], indent=2)}")
    
    try:
        response = requests.post(url, json=test['payload'])
        
        if response.status_code == 200:
            print("Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"FAILED. Status Code: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the server.")
        print("Make sure the Uvicorn server is running: 'uvicorn app.main:app --reload'")
        sys.exit(1)
        
    print("Waiting 5 seconds to avoid rate limits...")
    import time
    time.sleep(5)
    print("\n" + "="*50 + "\n")
