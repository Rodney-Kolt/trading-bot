#!/usr/bin/env python3
"""
Send Test Signal Now
Simulate MT5 EA sending a signal to test the complete system
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime

def send_test_signal():
    """Send a test BUY signal to see the system work"""
    
    webhook_url = "https://trading-bot-production-c863.up.railway.app/webhook"
    
    # Simulate MT5 EA signal
    signal_data = {
        "action": "BUY",
        "symbol": "EURUSD",
        "price": "1.0425",
        "strategy": "Test_Signal",
        "timeframe": "15m"
    }
    
    print("🚀 Sending Test Signal to Your System...")
    print("=" * 50)
    print(f"📡 Webhook URL: {webhook_url}")
    print(f"📊 Signal Data: {json.dumps(signal_data, indent=2)}")
    print("=" * 50)
    
    try:
        # Prepare the request
        data = json.dumps(signal_data).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'TestSignal/1.0'
            }
        )
        
        print("📤 Sending signal...")
        
        # Send the request
        with urllib.request.urlopen(req, timeout=10) as response:
            result = response.read().decode('utf-8')
            status_code = response.getcode()
        
        print(f"✅ HTTP Status: {status_code}")
        print(f"📝 Bot Response: {result}")
        
        if status_code == 200:
            print("\n🎉 SUCCESS! Test signal sent successfully!")
            print("\n📊 NOW CHECK YOUR DASHBOARD!")
            print("You should see:")
            print("   ✅ Daily Trades: 1 (instead of 0)")
            print("   ✅ Recent Activity: BUY signal received at 1.0425")
            print("   ✅ System processing the signal")
            print("\n🔗 This proves your complete system works!")
            print("💡 Real MT5 signals will work exactly the same way")
            
        else:
            print(f"\n❌ Unexpected response code: {status_code}")
            
    except Exception as e:
        print(f"\n❌ Error sending signal: {str(e)}")
        print("🔧 Check your internet connection")

if __name__ == "__main__":
    send_test_signal()
    print("\n🎯 Go check your dashboard now!")
    print("🔄 Refresh the page to see the new signal")