"""
Strict Domain Enforcement Test
Verify that:
- M001 (Amazon) ONLY accepts: automotive, beauty, books, electronics, fashion, grocery, sports, tech
- M001 REJECTS education
- B057 (Education Specialist) ONLY accepts education
- B057 REJECTS all other domains
"""

import os
import json
import sys

# Add the correct path for the app module
app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content-verify-&-decision-predict')
sys.path.insert(0, app_path)

from app.trained_model_analyzer import TrainedModelAnalyzer

# Load business profiles
with open('data/business_profiles.json') as f:
    business_profiles = json.load(f)

analyzer = TrainedModelAnalyzer()

print("=" * 80)
print("STRICT DOMAIN ENFORCEMENT TEST")
print("=" * 80)
print()

# Test cases
test_cases = [
    # M001 (Amazon) - Should ONLY allow: automotive, beauty, books, electronics, fashion, grocery, sports, tech
    {
        "name": "M001 - Electronics (ALLOWED)",
        "business_id": "M001",
        "text": "New AI-powered smart home devices with Alexa and machine learning",
        "expected_domain": "electronics",
        "should_approve": True
    },
    {
        "name": "M001 - Fashion (ALLOWED)",
        "business_id": "M001",
        "text": "Latest designer clothing collection with trendy outfits",
        "expected_domain": "fashion",
        "should_approve": True
    },
    {
        "name": "M001 - Tech (ALLOWED)",
        "business_id": "M001",
        "text": "Advanced software and coding solutions",
        "expected_domain": "tech",
        "should_approve": True
    },
    {
        "name": "M001 - EDUCATION (NOT ALLOWED) *** CRITICAL TEST ***",
        "business_id": "M001",
        "text": "Learn about our educational courses and training programs",
        "expected_domain": "education",
        "should_approve": False,
        "critical": True
    },
    {
        "name": "M001 - HEALTH (NOT ALLOWED)",
        "business_id": "M001",
        "text": "Medical services and healthcare solutions",
        "expected_domain": "health",
        "should_approve": False
    },
    
    # B057 (Education Specialist) - Should ONLY allow education
    {
        "name": "B057 - Education (ONLY DOMAIN ALLOWED)",
        "business_id": "B057",
        "text": "Learn about our educational courses and training programs",
        "expected_domain": "education",
        "should_approve": True
    },
    {
        "name": "B057 - Fashion (NOT ALLOWED)",
        "business_id": "B057",
        "text": "Latest designer clothing collection with trendy outfits",
        "expected_domain": "fashion",
        "should_approve": False
    },
    {
        "name": "B057 - Electronics (NOT ALLOWED)",
        "business_id": "B057",
        "text": "New AI-powered smart home devices",
        "expected_domain": "electronics",
        "should_approve": False
    },
    {
        "name": "B057 - Automotive (NOT ALLOWED)",
        "business_id": "B057",
        "text": "Best car and vehicle solutions",
        "expected_domain": "automotive",
        "should_approve": False
    },
    
    # Other allowed domains for M001
    {
        "name": "M001 - Automotive (ALLOWED)",
        "business_id": "M001",
        "text": "Best car and vehicle solutions",
        "expected_domain": "automotive",
        "should_approve": True
    },
    {
        "name": "M001 - Beauty (ALLOWED)",
        "business_id": "M001",
        "text": "Premium cosmetics and skincare products",
        "expected_domain": "beauty",
        "should_approve": True
    },
    {
        "name": "M001 - Books (ALLOWED)",
        "business_id": "M001",
        "text": "Bestselling novels and literature",
        "expected_domain": "books",
        "should_approve": True
    },
    {
        "name": "M001 - Grocery (ALLOWED)",
        "business_id": "M001",
        "text": "Fresh organic vegetables and fruits",
        "expected_domain": "grocery",
        "should_approve": True
    },
    {
        "name": "M001 - Sports (ALLOWED)",
        "business_id": "M001",
        "text": "Sports equipment and fitness gear",
        "expected_domain": "sports",
        "should_approve": True
    },
]

passed = 0
failed = 0
critical_failed = False

for i, test in enumerate(test_cases, 1):
    result = analyzer.analyze_content(
        user_text=test["text"],
        business_id=test["business_id"],
        registered_domain=test["expected_domain"]
    )
    
    is_critical = test.get("critical", False)
    
    # Determine if test passed
    predicted_category = result["detected_category"]
    is_approved = result["status"] == "Approved"
    
    # For this test, we care about whether it was approved or rejected
    # (not the exact predicted category)
    test_passed = (is_approved == test["should_approve"])
    
    status = "[PASS]" if test_passed else "[FAIL]"
    if test_passed:
        passed += 1
    else:
        failed += 1
        if is_critical:
            critical_failed = True
    
    critical_marker = " *** CRITICAL ***" if is_critical else ""
    
    print(f"{i}. {test['name']}{critical_marker}")
    print(f"   Business: {test['business_id']} | Domain: {test['expected_domain']}")
    print(f"   Predicted: {predicted_category} (conf: {result['confidence_score']*100:.2f}%)")
    print(f"   Result: {result['status']}")
    print(f"   Expected: {'Approved' if test['should_approve'] else 'Rejected'}")
    print(f"   {status}")
    print()

print("=" * 80)
print(f"RESULTS: {passed} Passed | {failed} Failed | {passed + failed} Total")
print(f"Success Rate: {100 * passed / (passed + failed):.1f}%")
if critical_failed:
    print()
    print("⚠️  CRITICAL TEST FAILED - Domain enforcement not working properly!")
    print("M001 should NEVER accept education posts!")
else:
    print()
    print("✓ All domain enforcement rules verified successfully!")
print("=" * 80)

sys.exit(0 if failed == 0 else 1)
