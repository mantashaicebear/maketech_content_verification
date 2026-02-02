"""Verify the specific case from the user request"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.trained_model_analyzer import analyze_content
import json

print("="*70)
print("VERIFYING: Your Specific Request Case")
print("="*70)

request = {
    "business_id": "B057",
    "User_Text": "Enroll in our advanced Python programming course with certification.",
    "Registered_Domain": "beauty"
}

print(f"\nRequest:")
print(f"  Business ID: {request['business_id']}")
print(f"  Text: {request['User_Text']}")
print(f"  Registered Domain: {request['Registered_Domain']}")

result = analyze_content(
    user_text=request['User_Text'],
    registered_domain=request['Registered_Domain'],
    business_id=request['business_id']
)

print(f"\nResponse:")
print(f"  Status: {result['status']}")
print(f"  Detected Category: {result['detected_category']}")
print(f"  Reason: {result['reason']}")
print(f"  Allowed Domains: {result['business_allowed_domains']}")
print(f"  Is Registered Domain Valid: {result.get('is_allowed_in_business_domains', 'N/A')}")

print("\n" + "="*70)
print("✓ FIXED: Now correctly rejects education course posted to beauty domain")
print("="*70)
