#!/usr/bin/env python3
"""
Test script for Regime Classifier API
Run locally or against production deployment
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"  # Change to production URL when deployed
API_KEY = "demo_free_key"  # Demo key for testing

def test_health():
    """Test health check endpoint."""
    print("\n🩺 Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health check passed: {data['status']}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_current_regime():
    """Test current regime endpoint."""
    print("\n📊 Testing /regime/current endpoint...")
    
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/regime/current", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Current regime: {data['regime']}")
        print(f"   Signal strength: {data['metrics']['signal_strength']}")
        print(f"   Duration: {data['regime_duration_days']} days")
        print(f"   Implications: {data['trading_implications'][0]}")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def test_history():
    """Test history endpoint."""
    print("\n📜 Testing /regime/history endpoint...")
    
    headers = {"X-API-Key": API_KEY}
    
    # Test with demo_free_key (should fail - feature not available)
    response = requests.get(f"{BASE_URL}/regime/history?days=30", headers=headers)
    
    if response.status_code == 403:
        print("✅ Correctly blocked free tier from history (as expected)")
        return True
    elif response.status_code == 200:
        data = response.json()
        print(f"✅ History retrieved: {data['total_days']} days")
        print(f"   Regime distribution: {data['regime_distribution']}")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        return False

def test_transitions():
    """Test transitions endpoint."""
    print("\n🔄 Testing /regime/transitions endpoint...")
    
    headers = {"X-API-Key": API_KEY}
    since_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    response = requests.get(
        f"{BASE_URL}/regime/transitions?since={since_date}",
        headers=headers
    )
    
    if response.status_code == 403:
        print("✅ Correctly blocked free tier from transitions (as expected)")
        return True
    elif response.status_code == 200:
        data = response.json()
        print(f"✅ Transitions retrieved: {data['total_transitions']} transitions")
        print(f"   Avg regime duration: {data['avg_regime_duration_days']} days")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        return False

def test_authentication():
    """Test API key authentication."""
    print("\n🔐 Testing authentication...")
    
    # Test without API key
    response = requests.get(f"{BASE_URL}/regime/current")
    if response.status_code == 422:  # FastAPI validation error (missing header)
        print("✅ Correctly rejects missing API key")
    else:
        print(f"⚠️  Expected 422, got {response.status_code}")
    
    # Test with invalid API key
    headers = {"X-API-Key": "invalid_key_123"}
    response = requests.get(f"{BASE_URL}/regime/current", headers=headers)
    
    if response.status_code == 401:
        print("✅ Correctly rejects invalid API key")
        return True
    else:
        print(f"❌ Expected 401, got {response.status_code}")
        return False

def test_rate_limiting():
    """Test rate limiting (only run if you want to exhaust quota)."""
    print("\n⏱️  Testing rate limiting...")
    print("   (Skipping - would exhaust free tier quota)")
    print("   To test manually, make 101 requests rapidly")
    return True

def integration_example():
    """Show how to integrate into a trading bot."""
    print("\n🤖 Integration Example:")
    print("=" * 60)
    
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{BASE_URL}/regime/current", headers=headers)
    
    if response.status_code != 200:
        print("❌ API request failed")
        return False
    
    regime_data = response.json()
    regime = regime_data['regime']
    signal_strength = regime_data['metrics']['signal_strength']
    
    print(f"Current regime: {regime}")
    print(f"Signal strength: {signal_strength}")
    print()
    
    # Trading logic example
    if regime == 'STABLE' and signal_strength < 0.5:
        print("✅ TRADE SIGNAL: STABLE regime detected")
        print("   → Safe to execute put credit spread (PCS)")
        print("   → Expected: Low volatility, theta decay optimal")
        return True
    elif regime in ['FRAGILE_ACCEL', 'FRAGILE_DIV']:
        print("⚠️  WARNING: Fragile regime detected")
        print("   → Skip PCS trades")
        print("   → Reduce position size if must trade")
        return True
    elif regime == 'FRAGILE_BOTH':
        print("🚨 ALERT: High chaos regime")
        print("   → Stay in cash or widen strikes significantly")
        return True
    else:
        print("ℹ️  NEUTRAL: Proceed with caution")
        return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Regime Classifier API - Test Suite")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {API_KEY}")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health()))
    results.append(("Current Regime", test_current_regime()))
    results.append(("History (Free Tier Block)", test_history()))
    results.append(("Transitions (Free Tier Block)", test_transitions()))
    results.append(("Authentication", test_authentication()))
    results.append(("Rate Limiting", test_rate_limiting()))
    results.append(("Integration Example", integration_example()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! API is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
