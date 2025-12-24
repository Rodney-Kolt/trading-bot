#!/usr/bin/env python3
"""
Test the profitable trading system locally
"""

import requests
import json
from datetime import datetime

BOT_URL = "https://trading-bot-production-c863.up.railway.app"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BOT_URL}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        # Check if it's the profitable system
        if data.get("system_type") == "profitable_trading_system":
            print("✅ Profitable system detected!")
        else:
            print("⚠️  Still showing basic system")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        return False

def test_automation():
    """Test automation endpoints"""
    print("\n🔍 Testing automation endpoints...")
    try:
        # Get current automation phase
        response = requests.get(f"{BOT_URL}/automation", timeout=10)
        print(f"GET /automation - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Current phase: {data.get('automation_phase', 'UNKNOWN')}")
            print("✅ Automation endpoint working!")
            return True
        else:
            print(f"❌ Automation endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Automation test failed: {e}")
        return False

def test_status():
    """Test enhanced status endpoint"""
    print("\n🔍 Testing enhanced status endpoint...")
    try:
        response = requests.get(f"{BOT_URL}/status", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            
            # Check for profitable system features
            if "automation_phase" in data:
                print("✅ Automation phase found in status")
            if "daily_stats" in data:
                print("✅ Daily stats found in status")
            if "profit_tracker" in data:
                print("✅ Profit tracker found in status")
            
            print(f"Automation Phase: {data.get('automation_phase', 'N/A')}")
            print(f"Emergency Stop: {data.get('emergency_stop', 'N/A')}")
            print(f"Daily Trades: {data.get('daily_stats', {}).get('trades', 'N/A')}")
            
            return True
        else:
            print(f"❌ Status test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status test failed: {e}")
        return False

def test_signal():
    """Test signal processing"""
    print("\n🔍 Testing signal processing...")
    try:
        test_signal_data = {
            "action": "BUY",
            "symbol": "EURUSD",
            "price": "1.1000",
            "strategy": "TEST",
            "reason": "SYSTEM_TEST",
            "timeframe": "15m"
        }
        
        response = requests.post(f"{BOT_URL}/webhook", 
                               json=test_signal_data, 
                               timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Check for profitable system response
            result = data.get("result", {})
            if "automation_phase" in result:
                print("✅ Profitable system signal processing detected!")
                print(f"Automation Phase: {result.get('automation_phase')}")
                return True
            else:
                print("⚠️  Basic system signal processing detected")
                return False
        else:
            print(f"❌ Signal test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Signal test failed: {e}")
        return False

def main():
    print("🚀 Testing Profitable Trading System")
    print(f"🎯 Bot URL: {BOT_URL}")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Automation Endpoints", test_automation),
        ("Enhanced Status", test_status),
        ("Signal Processing", test_signal)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED - Profitable system is deployed!")
        print("🎯 Next steps:")
        print("   1. Compile ProfitableEA.mq5 in MT5")
        print("   2. Update dashboard deployment")
        print("   3. Test complete system integration")
    else:
        print("⚠️  SOME TESTS FAILED - System may still be deploying")
        print("🔄 Railway auto-deployment may still be in progress")
        print("⏳ Wait a few minutes and test again")

if __name__ == "__main__":
    main()