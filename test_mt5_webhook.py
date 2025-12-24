#!/usr/bin/env python3
"""
Test MT5 Webhook Connection
Simulates what the MT5 EA will send to verify the connection works
"""

import requests
import json

def test_webhook():
    """Test the webhook endpoint with a simulated MT5 signal"""
    
    webhook_url = "https://trading-bot-production-c863.up.railway.app/webhook"
    
    # Simulate MT5 EA signal
    test_signal = {
        "action": "BUY",
        "symbol": "EURUSD",
        "price": "1.0850",
        "strategy": "Profitable_EMA_RSI",
        "timeframe": "15m"
    }
    
    print("🧪 Testing MT5 Webhook Connection...")
    print(f"📡 URL: {webhook_url}")
    print(f"📊 Signal: {test_signal}")
    
    try:
        response = requests.post(
            webhook_url,
            json=test_signal,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"✅ Response Code: {response.status_code}")
        print(f"📝 Response: {response.text}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS! Webhook is working perfectly!")
            print("🔗 Your MT5 EA will be able to send signals to the Python bot")
            return True
        else:
            print("❌ Webhook test failed")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False

if __name__ == "__main__":
    test_webhook()