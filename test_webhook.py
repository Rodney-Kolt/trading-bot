"""
Test script to simulate TradingView webhook calls
Use this to test your bot before connecting real alerts
"""

import requests
import json
import time

# Bot webhook URL
WEBHOOK_URL = "http://localhost:5000/webhook"

# Test signals
test_signals = [
    {
        "action": "BUY",
        "symbol": "BTCUSDT",
        "price": "50000"
    },
    {
        "action": "SELL", 
        "symbol": "BTCUSDT",
        "price": "51000"
    }
]

def test_webhook():
    """Send test signals to bot"""
    print("🧪 Testing Trading Bot Webhook...")
    
    for i, signal in enumerate(test_signals, 1):
        print(f"\n📡 Sending test signal {i}: {signal}")
        
        try:
            response = requests.post(
                WEBHOOK_URL,
                json=signal,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"✅ Response: {response.status_code}")
            print(f"📄 Data: {response.json()}")
            
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed - is the bot running?")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Wait between signals
        if i < len(test_signals):
            print("⏳ Waiting 3 seconds...")
            time.sleep(3)

def test_status():
    """Check bot status"""
    print("\n📊 Checking bot status...")
    
    try:
        response = requests.get(f"http://localhost:5000/status")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Data: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🤖 Trading Bot Test Suite")
    print("Make sure your bot is running first!")
    print("python app.py")
    
    input("\nPress Enter to start tests...")
    
    test_webhook()
    test_status()
    
    print("\n✅ Tests completed!")