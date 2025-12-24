#!/usr/bin/env python3
"""
Manual Signal Test - Simulate MT5 EA Signal
This will test if your webhook and dashboard are working
"""

import json
import urllib.request
import urllib.parse

def send_test_signal():
    """Send a test signal to verify the webhook works"""
    
    webhook_url = "https://trading-bot-production-c863.up.railway.app/webhook"
    
    # Test signal data (simulates MT5 EA)
    signal_data = {
        "action": "BUY",
        "symbol": "EURUSD", 
        "price": "1.0850",
        "strategy": "Manual_Test",
        "timeframe": "15m"
    }
    
    print("🧪 Sending Manual Test Signal...")
    print(f"📡 URL: {webhook_url}")
    print(f"📊 Data: {signal_data}")
    
    try:
        # Prepare the request
        data = json.dumps(signal_data).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Send the request
        with urllib.request.urlopen(req, timeout=10) as response:
            result = response.read().decode('utf-8')
            status_code = response.getcode()
            
        print(f"✅ Response Code: {status_code}")
        print(f"📝 Response: {result}")
        
        if status_code == 200:
            print("\n🎉 SUCCESS! Manual signal sent!")
            print("📊 Check your dashboard - you should see:")
            print("   - Daily Trades: 1")
            print("   - Recent Activity: BUY signal received")
            print("\n🔗 This proves your webhook is working!")
            print("💡 The issue is likely that MT5 EA isn't generating signals yet")
        else:
            print(f"\n❌ Failed with status code: {status_code}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("🔧 This suggests a connection problem")

if __name__ == "__main__":
    send_test_signal()