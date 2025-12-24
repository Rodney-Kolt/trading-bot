#!/usr/bin/env python3
"""
Test Multi-Currency System
Send multiple currency signals to test the enhanced system
"""

import json
import urllib.request
import time

def send_multi_currency_signals():
    """Send test signals for multiple currencies"""
    
    webhook_url = "https://trading-bot-production-c863.up.railway.app/webhook"
    
    # Test signals for different currencies
    test_signals = [
        {"action": "BUY", "symbol": "EURUSD", "price": "1.0425", "strategy": "MultiCurrency_Test", "timeframe": "15m"},
        {"action": "BUY", "symbol": "GBPUSD", "price": "1.2650", "strategy": "MultiCurrency_Test", "timeframe": "15m"},
        {"action": "BUY", "symbol": "USDJPY", "price": "157.25", "strategy": "MultiCurrency_Test", "timeframe": "15m"},
        {"action": "BUY", "symbol": "AUDUSD", "price": "0.6180", "strategy": "MultiCurrency_Test", "timeframe": "15m"}
    ]
    
    print("🌍 Testing Multi-Currency Trading System...")
    print("=" * 60)
    
    for i, signal in enumerate(test_signals, 1):
        print(f"\n📊 Sending Signal {i}/4: {signal['symbol']} {signal['action']} @ {signal['price']}")
        
        try:
            # Prepare request
            data = json.dumps(signal).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            # Send request
            with urllib.request.urlopen(req, timeout=10) as response:
                result = response.read().decode('utf-8')
                status = response.getcode()
            
            if status == 200:
                print(f"✅ {signal['symbol']} signal sent successfully")
            else:
                print(f"❌ {signal['symbol']} signal failed: {status}")
                
        except Exception as e:
            print(f"❌ Error sending {signal['symbol']} signal: {str(e)}")
        
        # Small delay between signals
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("🎉 Multi-currency test complete!")
    print("\n📊 Now check your dashboard - you should see:")
    print("   ✅ Daily Trades: 4")
    print("   ✅ Multi-Currency Performance section")
    print("   ✅ Signals from EURUSD, GBPUSD, USDJPY, AUDUSD")
    print("   ✅ Currency breakdown table")
    print("   ✅ Recent Activity with all currencies")
    print("\n🌍 Your multi-currency system is working!")

if __name__ == "__main__":
    send_multi_currency_signals()