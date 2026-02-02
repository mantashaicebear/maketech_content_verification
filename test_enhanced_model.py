"""
Test Enhanced Model with Multi-Domain Businesses
"""

import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'content-verify-&-decision-predict'))

from app.trained_model_analyzer import TrainedModelAnalyzer

def test_enhanced_model():
    """Test the enhanced model with real Indian business scenarios"""
    
    analyzer = TrainedModelAnalyzer()
    
    # Load business profiles to get the new multi-domain IDs
    business_profiles_path = os.path.join(os.path.dirname(__file__), 'data', 'business_profiles.json')
    with open(business_profiles_path) as f:
        business_profiles = json.load(f)
    
    # Get IDs for multi-domain businesses (they start with 'M')
    multi_domain_ids = {v['name']: k for k, v in business_profiles.items() if k.startswith('M')}
    amazon_id = multi_domain_ids.get('Amazon India', 'M001')
    myntra_id = multi_domain_ids.get('Myntra', 'M005')
    flipkart_id = multi_domain_ids.get('Flipkart', 'M002')
    swiggy_id = multi_domain_ids.get('Swiggy', 'M006')
    nykaa_id = multi_domain_ids.get('Nykaa', 'M010')
    makemytrip_id = [k for k, v in business_profiles.items() if 'travel' in v.get('domains', []) and k.startswith('M')][0] if any('travel' in v.get('domains', []) for k, v in business_profiles.items() if k.startswith('M')) else 'M004'
    
    print("\n" + "="*80)
    print("TESTING ENHANCED MODEL - INDIAN MULTI-DOMAIN BUSINESSES")
    print("="*80 + "\n")
    
    test_cases = [
        {
            "name": "Amazon India - Electronics (Allowed)",
            "text": "New AI-powered smart home devices with Alexa and machine learning features",
            "domain": "electronics",
            "business_id": amazon_id,
            "expected": "Approved"
        },
        {
            "name": "Amazon India - Fashion (Allowed)",
            "text": "Latest designer clothing collection with trendy outfits and accessories",
            "domain": "fashion",
            "business_id": amazon_id,
            "expected": "Approved"
        },
        {
            "name": "Amazon India - Grocery (Allowed)",
            "text": "Fresh organic vegetables and fruits delivered daily to your home",
            "domain": "grocery",
            "business_id": amazon_id,
            "expected": "Approved"
        },
        {
            "name": "Myntra - Fashion (Allowed)",
            "text": "Exclusive fashion trends and designer wear for style enthusiasts",
            "domain": "fashion",
            "business_id": myntra_id,
            "expected": "Approved"
        },
        {
            "name": "Myntra - Electronics (NOT Allowed - Cross Domain)",
            "text": "Latest laptops and smartphones with advanced technology",
            "domain": "electronics",
            "business_id": myntra_id,
            "expected": "Rejected"
        },
        {
            "name": "Swiggy - Food (Allowed)",
            "text": "Delicious restaurant meals and cuisine delivered hot to your doorstep",
            "domain": "food",
            "business_id": swiggy_id,
            "expected": "Approved"
        },
        {
            "name": "Swiggy - Automotive (NOT Allowed - Cross Domain)",
            "text": "Best car and vehicle solutions for automotive needs",
            "domain": "automotive",
            "business_id": swiggy_id,
            "expected": "Rejected"
        },
        {
            "name": "Flipkart - Books (Allowed)",
            "text": "Bestselling novels and literature for reading enthusiasts",
            "domain": "books",
            "business_id": flipkart_id,
            "expected": "Approved"
        },
        {
            "name": "Any Business - Gambling (Restricted)",
            "text": "Casino betting and poker gambling opportunities available",
            "domain": "gambling",
            "business_id": amazon_id,
            "expected": "Rejected"
        },
        {
            "name": "Any Business - Weapons (Restricted)",
            "text": "Firearms and rifles for sale with ammunition",
            "domain": "weapons",
            "business_id": flipkart_id,
            "expected": "Rejected"
        },
        {
            "name": "Nykaa - Beauty (Allowed)",
            "text": "Premium cosmetics and skincare products for beauty lovers",
            "domain": "beauty",
            "business_id": nykaa_id,
            "expected": "Approved"
        },
        {
            "name": "MakeMyTrip - Travel (Allowed)",
            "text": "Book your dream vacation with flight and hotel packages",
            "domain": "travel",
            "business_id": makemytrip_id,
            "expected": "Approved"
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   Text: \"{test['text'][:60]}...\"")
        print(f"   Domain: {test['domain']} | Business: {test['business_id']}")
        
        # Analyze content
        result = analyzer.analyze_content(
            user_text=test['text'],
            registered_domain=test['domain'],
            business_id=test.get('business_id')
        )
        
        # Check result
        actual_status = result.get('status', 'Unknown')
        predicted_category = result.get('predicted_category', 'Unknown')
        confidence = result.get('confidence', 0.0)
        
        print(f"   Predicted Category: {predicted_category}")
        print(f"   Confidence: {confidence:.2%}")
        print(f"   Status: {actual_status}")
        print(f"   Expected: {test['expected']}")
        
        # Verify
        # Accept partial matches for rejection statuses
        if test['expected'] == "Rejected" and "Rejected" in actual_status:
            print(f"   [PASS]")
            passed += 1
        elif actual_status == test['expected']:
            print(f"   [PASS]")
            passed += 1
        else:
            print(f"   [FAIL] (Expected {test['expected']}, Got {actual_status})")
            failed += 1
    
    print("\n" + "="*80)
    print(f"TEST RESULTS: {passed} Passed | {failed} Failed | {passed+failed} Total")
    print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_enhanced_model()
