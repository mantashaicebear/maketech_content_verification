"""Verify user's specific test case is now fixed"""
import sys
import os

app_path = r'd:\Internship work\maketech\maketech_content_verification\content-verify-&-decision-predict'
sys.path.insert(0, app_path)

from app.trained_model_analyzer import TrainedModelAnalyzer

analyzer = TrainedModelAnalyzer()

print("="*70)
print("VERIFYING USER'S SPECIFIC TEST CASE")
print("="*70)

# User's exact test case
result = analyzer.analyze_content(
    user_text='New AI-powered smart home devices with Alexa integration.',
    registered_domain='beauty',
    business_id='M001'
)

print(f"\nUser Request:")
print(f"  Business ID: M001")
print(f"  Text: New AI-powered smart home devices with Alexa integration.")
print(f"  Registered Domain: beauty")

print(f"\nResponse:")
print(f"  Status: {result['status']}")
print(f"  Detected Category: {result['detected_category']}")
print(f"  Reason: {result['reason']}")

if result['status'] == 'Rejected: Domain Mismatch':
    print(f"\n✓ FIXED: Request is now correctly REJECTED")
    print(f"  → Electronics content cannot be posted to beauty domain")
    print(f"  → Even though M001 allows both electronics AND beauty")
else:
    print(f"\n✗ FAILED: Request should be rejected but got: {result['status']}")

print("\n" + "="*70)
print("Additional Test Cases")
print("="*70)

test_cases = [
    {
        'name': 'M001: Correct domain match (electronics content → electronics domain)',
        'text': 'New AI-powered smart home devices with Alexa integration.',
        'registered_domain': 'electronics',
        'business_id': 'M001',
        'expected': 'Approved'
    },
    {
        'name': 'M001: Correct domain match (beauty content → beauty domain)',
        'text': 'Premium makeup and skincare products now available.',
        'registered_domain': 'beauty',
        'business_id': 'M001',
        'expected': 'Approved'
    },
    {
        'name': 'M001: Wrong domain (books content → electronics domain)',
        'text': 'Check out our latest novel and publication collection.',
        'registered_domain': 'electronics',
        'business_id': 'M001',
        'expected': 'Rejected: Domain Mismatch'
    },
]

passed = 0
failed = 0

for test_case in test_cases:
    result = analyzer.analyze_content(
        user_text=test_case['text'],
        registered_domain=test_case['registered_domain'],
        business_id=test_case['business_id']
    )
    
    print(f"\n✓ {test_case['name']}")
    print(f"  Status: {result['status']}")
    
    if test_case['expected'] in result['status']:
        print(f"  Result: PASS")
        passed += 1
    else:
        print(f"  Expected: {test_case['expected']}")
        print(f"  Result: FAIL")
        failed += 1

print(f"\n" + "="*70)
print(f"Summary: {passed} Passed, {failed} Failed")
print("="*70)
