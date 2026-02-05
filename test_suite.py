#!/usr/bin/env python3
"""
Automated Test Suite for Scam Message Honeypot API
Run this script to validate API functionality
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"
API_KEY = "TEST_API_KEY"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

test_results = {
    "passed": 0,
    "failed": 0,
    "total": 0,
    "details": []
}

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_test(name, passed, details=""):
    status = "PASS" if passed else "FAIL"
    print(f"{status} | {name}")
    if details:
        print(f"         {details}")
    
    test_results["total"] += 1
    if passed:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1
    
    test_results["details"].append({
        "test": name,
        "passed": passed,
        "details": details,
        "timestamp": datetime.utcnow().isoformat()
    })

def assert_status(response, expected_status, test_name):
    actual = response.status_code
    if actual == expected_status:
        print_test(test_name, True, f"Status: {actual}")
        return True
    else:
        print_test(test_name, False, f"Expected {expected_status}, got {actual}")
        return False

def assert_json_field(data, field, test_name):
    if field in data:
        print_test(test_name, True, f"Field '{field}' present")
        return True
    else:
        print_test(test_name, False, f"Field '{field}' missing")
        return False

def test_health_check():
    print_header("TEST 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/honeypot/health", timeout=5)
        assert_status(response, 200, "Health check returns 200")
        data = response.json()
        assert_json_field(data, "status", "Response has status field")
        assert_json_field(data, "timestamp", "Response has timestamp field")
    except Exception as e:
        print_test("Health check", False, str(e))

def test_legitimate_message():
    print_header("TEST 2: Legitimate Message")
    try:
        payload = {"agent": "test-suite", "payload": "Hello, can you help me?"}
        response = requests.post(f"{BASE_URL}/api/honeypot/message", 
                                json=payload, headers=HEADERS, timeout=5)
        assert_status(response, 200, "Request processed successfully")
        data = response.json()
        assert_json_field(data, "status", "Response has status")
        assert_json_field(data, "trap", "Response has trap")
        assert_json_field(data, "scamScore", "Response has scamScore")
        if data.get("scamScore", 100) < 40:
            print_test("Low scam score for legitimate message", True, 
                      f"Score: {data.get('scamScore')}")
    except Exception as e:
        print_test("Legitimate message test", False, str(e))

def test_high_scam_score():
    print_header("TEST 3: High Scam Score Detection")
    try:
        payload = {
            "agent": "test-suite",
            "payload": "URGENT! Verify OTP immediately: http://fakebank.com"
        }
        response = requests.post(f"{BASE_URL}/api/honeypot/message",
                                json=payload, headers=HEADERS, timeout=5)
        assert_status(response, 200, "High-scam message processed")
        data = response.json()
        if data.get("scamScore", 0) > 40:
            print_test("High scam score detected", True, f"Score: {data.get('scamScore')}")
    except Exception as e:
        print_test("High scam score test", False, str(e))

def test_missing_auth():
    print_header("TEST 4: Missing Authentication Header")
    try:
        payload = {"agent": "test-suite", "payload": "test"}
        response = requests.post(f"{BASE_URL}/api/honeypot/message",
                                json=payload, timeout=5)
        assert_status(response, 401, "Missing auth returns 401")
    except Exception as e:
        print_test("Missing auth header test", False, str(e))

def test_invalid_api_key():
    print_header("TEST 5: Invalid API Key")
    try:
        bad_headers = {
            "Authorization": "Bearer WRONG_KEY",
            "Content-Type": "application/json"
        }
        payload = {"agent": "test-suite", "payload": "test"}
        response = requests.post(f"{BASE_URL}/api/honeypot/message",
                                json=payload, headers=bad_headers, timeout=5)
        assert_status(response, 403, "Invalid API key returns 403")
    except Exception as e:
        print_test("Invalid API key test", False, str(e))

def test_missing_payload():
    print_header("TEST 6: Missing Payload Field")
    try:
        payload = {"agent": "test-suite"}
        response = requests.post(f"{BASE_URL}/api/honeypot/message",
                                json=payload, headers=HEADERS, timeout=5)
        assert_status(response, 400, "Missing payload returns 400")
    except Exception as e:
        print_test("Missing payload test", False, str(e))

def test_get_logs():
    print_header("TEST 7: Retrieve Logs")
    try:
        response = requests.get(f"{BASE_URL}/api/honeypot/logs",
                               headers=HEADERS, timeout=5)
        assert_status(response, 200, "Get logs returns 200")
        data = response.json()
        assert_json_field(data, "status", "Response has status")
        assert_json_field(data, "count", "Response has count")
        assert_json_field(data, "logs", "Response has logs")
    except Exception as e:
        print_test("Get logs test", False, str(e))

def test_unknown_endpoint():
    print_header("TEST 8: Unknown Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/api/honeypot/unknown",
                               headers=HEADERS, timeout=5)
        assert_status(response, 404, "Unknown endpoint returns 404")
    except Exception as e:
        print_test("Unknown endpoint test", False, str(e))

def run_all_tests():
    print("\n" + "=" * 70)
    print("SCAM MESSAGE HONEYPOT API - TEST SUITE")
    print("=" * 70)
    
    print(f"\nBase URL: {BASE_URL}")
    print(f"Starting tests at {datetime.utcnow().isoformat()}")
    
    test_health_check()
    test_legitimate_message()
    test_high_scam_score()
    test_missing_auth()
    test_invalid_api_key()
    test_missing_payload()
    test_get_logs()
    test_unknown_endpoint()
    
    # Print summary
    print_header("TEST SUMMARY")
    print(f"Passed: {test_results['passed']}/{test_results['total']}")
    print(f"Failed: {test_results['failed']}/{test_results['total']}")
    
    if test_results['failed'] == 0:
        print("\nALL TESTS PASSED - API IS OPERATIONAL")
    else:
        print(f"\n{test_results['failed']} TEST(S) FAILED")
    
    print("=" * 70 + "\n")
    
    # Save results
    with open("test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)
    
    return test_results['failed'] == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        exit(1)
