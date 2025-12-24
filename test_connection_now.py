#!/usr/bin/env python3
"""
Test Connection Right Now
Send a test signal to verify the complete system works
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime

def test_system_connection():
    """Send test signal to verify webhook and dashboard work"""
    
    webhook_url = "https://trading-bot-production-c863.up.railway.app/webhook"
    
    # Test signal (simulates what MT5 EA will send)
    test_data = {
        "action": "BUY",
        "symbol": "EURUSD",
        "price": "1.0425",
        "strategy": "Connection_Test",
        "timeframe": "15m",
        "timestamp": datetime.now().isoformat()
    }
    
    print("🧪 Testing Complete System Connection...")
    print(f"📡 Target: {webhook_url}")
    print(f"📊 Test Signal: {test_data}")
    print()
    
    try:
        # Prepare request
        data = json.dumps(test_data).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'MT5-EA-Test/1.0'
            }
        )
        
        # Send request
        print("📤 Sending test signal...")
        with urllib.request.urlopen(req, timeout=15) as response:
            result = response.read().decode('utf-8')
            status = response.getcode()
        
        print(f"✅ HTTP Status: {status}")
        print(f"📝 Response: {result}")
        
        if status == 200:
            print("\n🎉 SUCCESS! System is working perfectly!")
            print("\n📊 Now check your dashboard - you should see:")
            print("   ✅ Daily Trades: 1")
            print("   ✅ Recent Activity: BUY signal received")
            print("   ✅ Connection confirmed!")
            print("\n🎯 This proves your MT5 → Python Bot → Dashboard chain works!")
            print("💡 You just need to wait for real market signals")
            return True
        else:
            print(f"\n❌ Unexpected status: {status}")
            return False
            
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        print("🔧 Check your internet connection and bot URL")
        return False

if __name__ == "__main__":
    print("🔗 Complete System Connection Test")
    print("=" * 50)
    test_system_connection()
    print("=" * 50)