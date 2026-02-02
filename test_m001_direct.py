"""Test M001 directly"""
import sys
import os

# Set up paths properly
app_path = r'd:\Internship work\maketech\maketech_content_verification\content-verify-&-decision-predict'
sys.path.insert(0, app_path)

from app.trained_model_analyzer import TrainedModelAnalyzer

analyzer = TrainedModelAnalyzer()

print("="*70)
print("Testing M001 Content-Domain Mismatch")
print("="*70)

test_cases = [
    {
        'name': 'M001: Smart home (electronics) posted to beauty domain',
        'text': 'New AI-powered smart home devices with Alexa integration.',
        'registered_domain': 'beauty',
        'business_id': 'M001',
    },
    {
        'name': 'M001: Beauty content posted to beauty domain',
        'text': 'Premium makeup services available now with discount.',
        'registered_domain': 'beauty',
        'business_id': 'M001',
    },
    {
        'name': 'M001: Electronics content posted to electronics domain',
        'text': 'New AI-powered smart home devices with Alexa integration.',
        'registered_domain': 'electronics',
        'business_id': 'M001',
    },
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test_case['name']}")
    print(f"  Text: {test_case['text']}")
    print(f"  Registered Domain: {test_case['registered_domain']}")
    print(f"  Business ID: {test_case['business_id']}")
    
    result = analyzer.analyze_content(
        user_text=test_case['text'],
        registered_domain=test_case['registered_domain'],
        business_id=test_case['business_id']
    )
    
    print(f"  Status: {result['status']}")
    print(f"  Detected Category: {result['detected_category']}")
    print(f"  Confidence: {result['confidence']:.2%}")
    print(f"  Reason: {result['reason']}")
