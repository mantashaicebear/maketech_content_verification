"""
End-to-End Integration Test: Domain Enforcement in API
Tests that the API correctly enforces business domain restrictions
"""

import requests
import json
import time
import subprocess
import os
import signal
import sys

def test_api_domain_enforcement():
    """Test domain enforcement through the API"""
    
    # Test cases with business IDs and content
    test_cases = [
        {
            "name": "M001 (Amazon) - Electronics POST (Allowed)",
            "business_id": "M001",
            "content": "New AI-powered smart home devices with Alexa integration",
            "should_approve": True
        },
        {
            "name": "M001 (Amazon) - EDUCATION POST (BLOCKED) *** CRITICAL ***",
            "business_id": "M001",
            "content": "Learn Python programming with our online course",
            "should_approve": False,
            "critical": True
        },
        {
            "name": "B057 (Education) - Education POST (Allowed)",
            "business_id": "B057",
            "content": "Advanced Python programming course for beginners",
            "should_approve": True
        },
        {
            "name": "B057 (Education) - Fashion POST (BLOCKED)",
            "business_id": "B057",
            "content": "Latest designer clothing collection with trendy outfits",
            "should_approve": False
        },
        {
            "name": "M005 (Myntra) - Fashion POST (Allowed)",
            "business_id": "M005",
            "content": "Exclusive fashion collection with latest trends",
            "should_approve": True
        },
        {
            "name": "M005 (Myntra) - Electronics POST (BLOCKED)",
            "business_id": "M005",
            "content": "New smartphones and laptops with latest technology",
            "should_approve": False
        },
    ]
    
    print("=" * 80)
    print("END-TO-END API DOMAIN ENFORCEMENT TEST")
    print("=" * 80)
    print()
    
    api_url = "http://127.0.0.1:8000/analyze"
    
    passed = 0
    failed = 0
    critical_failed = False
    
    for i, test_case in enumerate(test_cases, 1):
        is_critical = test_case.get("critical", False)
        critical_marker = " *** CRITICAL ***" if is_critical else ""
        
        try:
            # Make API request
            payload = {
                "business_id": test_case["business_id"],
                "user_text": test_case["content"]
            }
            
            response = requests.post(api_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # Determine if test passed
                status = result.get("status", "")
                is_approved = "Approved" in status
                test_passed = (is_approved == test_case["should_approve"])
                
                status_badge = "[PASS]" if test_passed else "[FAIL]"
                if test_passed:
                    passed += 1
                else:
                    failed += 1
                    if is_critical:
                        critical_failed = True
                
                print(f"{i}. {test_case['name']}{critical_marker}")
                print(f"   Business: {test_case['business_id']}")
                print(f"   Content: {test_case['content'][:60]}...")
                print(f"   Result: {status}")
                print(f"   Reason: {result.get('reason', 'N/A')}")
                print(f"   Expected: {'Approved' if test_case['should_approve'] else 'Rejected'}")
                print(f"   {status_badge}")
                print()
            else:
                print(f"{i}. {test_case['name']}{critical_marker}")
                print(f"   ERROR: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                print(f"   [FAIL]")
                print()
                failed += 1
                if is_critical:
                    critical_failed = True
                
        except Exception as e:
            print(f"{i}. {test_case['name']}{critical_marker}")
            print(f"   ERROR: {str(e)}")
            print(f"   [FAIL]")
            print()
            failed += 1
            if is_critical:
                critical_failed = True
    
    print("=" * 80)
    print(f"RESULTS: {passed} Passed | {failed} Failed | {passed + failed} Total")
    print(f"Success Rate: {100 * passed / (passed + failed):.1f}%")
    if critical_failed:
        print()
        print("⚠️  CRITICAL TEST FAILED - Domain enforcement not working properly!")
    else:
        print()
        print("✓ All API domain enforcement tests passed!")
    print("=" * 80)
    
    return failed == 0

if __name__ == "__main__":
    print("Waiting 3 seconds for API server to be ready...")
    time.sleep(3)
    
    try:
        success = test_api_domain_enforcement()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Test failed with error: {e}")
        sys.exit(1)
