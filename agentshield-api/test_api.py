"""
Test script for AgentShield API
"""

import requests
import json

# Test locally
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_validate_safe_token():
    """Test with a known safe token (USDC on Base)"""
    print("\n=== Testing Safe Token (USDC on Base) ===")
    payload = {
        "token_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "chain": "base",
        "amount": "1.0"
    }
    response = requests.post(f"{BASE_URL}/validate-token", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_validate_honeypot():
    """Test with our known honeypot on Cronos testnet"""
    print("\n=== Testing Honeypot Token (Cronos Testnet) ===")
    payload = {
        "token_address": "0x6001B76e8CeA99a749F591ed6E1cE7a704CF231b",
        "chain": "cronos-testnet",
        "amount": "1.0"
    }
    response = requests.post(f"{BASE_URL}/validate-token", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    # Verify it's detected as HIGH risk
    if result.get("risk_level") == "HIGH":
        print("✅ Honeypot correctly detected!")
        return True
    else:
        print("❌ Honeypot NOT detected!")
        return False

def test_invalid_address():
    """Test with invalid address"""
    print("\n=== Testing Invalid Address ===")
    payload = {
        "token_address": "0xinvalid",
        "chain": "ethereum",
        "amount": "1.0"
    }
    response = requests.post(f"{BASE_URL}/validate-token", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

if __name__ == "__main__":
    print("🧪 AgentShield API Test Suite")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Safe Token", test_validate_safe_token),
        ("Honeypot Detection", test_validate_honeypot),
        ("Invalid Address", test_invalid_address),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
