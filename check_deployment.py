#!/usr/bin/env python3
"""
Deployment Checker - Verify your bot is working correctly
Run this after deploying to Railway to test everything
"""

import requests
import json
import time
import sys

def test_endpoint(url, description, expected_status=200):
    """Test an endpoint and return result"""
    print(f"🔍 Testing {description}...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == expected_status:
            print(f"✅ {description} - OK ({response.status_code})")
            return True, response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        else:
            print(f"❌ {description} - Failed ({response.status_code})")
            return False, response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ {description} - Connection failed: {str(e)}")
        return False, str(e)

def test_webhook(base_url):
    """Test webhook endpoint with sample data"""
    webhook_url = f"{base_url}/webhook"
    test_data = {
        "action": "BUY",
        "symbol": "BTCUSDT",
        "price": "50000",
        "strategy": "EMA_RSI",
        "timeframe": "15m"
    }
    
    print(f"🔍 Testing webhook with sample data...")
    try:
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Webhook test - OK ({response.status_code})")
            result = response.json()
            print(f"   Response: {result}")
            return True, result
        else:
            print(f"❌ Webhook test - Failed ({response.status_code})")
            print(f"   Response: {response.text}")
            return False, response.text
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Webhook test - Connection failed: {str(e)}")
        return False, str(e)

def main():
    print("🤖 Trading Bot Deployment Checker")
    print("=" * 50)
    
    # Get Railway URL from user
    base_url = input("Enter your Railway app URL (e.g., https://your-app.railway.app): ").strip()
    
    if not base_url:
        print("❌ No URL provided. Exiting.")
        sys.exit(1)
    
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')
    
    print(f"\n🎯 Testing deployment at: {base_url}")
    print("-" * 50)
    
    # Test 1: Health endpoint
    health_ok, health_data = test_endpoint(f"{base_url}/health", "Health Check")
    
    # Test 2: Status endpoint
    status_ok, status_data = test_endpoint(f"{base_url}/status", "Status Check")
    
    # Test 3: Webhook endpoint
    webhook_ok, webhook_data = test_webhook(base_url)
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("-" * 30)
    
    tests = [
        ("Health Endpoint", health_ok),
        ("Status Endpoint", status_ok),
        ("Webhook Endpoint", webhook_ok)
    ]
    
    passed = sum(1 for _, ok in tests if ok)
    total = len(tests)
    
    for test_name, ok in tests:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your bot is deployed correctly.")
        print("\n📋 Next steps:")
        print("1. Set up TradingView alerts")
        print("2. Configure Pine Script strategy")
        print("3. Start with paper trading (SANDBOX_MODE=true)")
        print("4. Monitor logs and performance")
        
        print(f"\n🔗 Important URLs:")
        print(f"Health Check: {base_url}/health")
        print(f"Bot Status:   {base_url}/status")
        print(f"Webhook:      {base_url}/webhook")
        
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check your deployment:")
        print("1. Verify Railway app is running")
        print("2. Check environment variables")
        print("3. Review deployment logs")
        print("4. Ensure all dependencies are installed")
    
    print(f"\n💡 Tip: You can run this checker anytime to verify your bot is working.")

if __name__ == "__main__":
    main()