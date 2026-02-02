"""Test M001 electronics/beauty mismatch"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.trained_model_analyzer import analyze_content
import json

print("="*70)
print("Testing M001 Content-Domain Mismatch")
print("="*70)

test_cases = [
    {
        'name': 'M001: Smart home (electronics) posted to beauty domain',
        'text': 'New AI-powered smart home devices with Alexa integration.',
        'registered_domain': 'beauty',
        'business_id': 'M001',
        'expected_status': 'Rejected: Domain Mismatch'
    },
    {
        'name': 'M001: Beauty content posted to beauty domain',
        'text': 'Premium makeup services available now with discount.',
        'registered_domain': 'beauty',
        'business_id': 'M001',
        'expected_status': 'Approved'
    },
    {
        'name': 'M001: Electronics content posted to electronics domain',
        'text': 'New AI-powered smart home devices with Alexa integration.',
        'registered_domain': 'electronics',
        'business_id': 'M001',
        'expected_status': 'Approved'
    },
]

passed_count = 0
failed_count = 0

for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test_case['name']}")
    print(f"  Text: {test_case['text']}")
    print(f"  Registered Domain: {test_case['registered_domain']}")
    print(f"  Business ID: {test_case['business_id']}")
    print(f"  Expected: {test_case['expected_status']}")
    
    result = analyze_content(
        user_text=test_case['text'],
        registered_domain=test_case['registered_domain'],
        business_id=test_case['business_id']
    )
    
    actual_status = result['status']
    detected_category = result['detected_category']
    confidence = result['confidence']
    
    print(f"  Actual: {actual_status}")
    print(f"  Detected Category: {detected_category}")
    print(f"  Confidence: {confidence:.2%}")
    print(f"  Reason: {result['reason']}")
    
    # Check if test passed
    passed = actual_status == test_case['expected_status']
    print(f"  Result: {'✓ PASS' if passed else '✗ FAIL'}")
    
    if passed:
        passed_count += 1
    else:
        failed_count += 1

print("\n" + "="*70)
print(f"SUMMARY: {passed_count} Passed, {failed_count} Failed")
print("="*70)
