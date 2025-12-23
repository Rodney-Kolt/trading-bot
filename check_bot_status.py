#!/usr/bin/env python3
"""
Quick Bot Status Checker
Run this to diagnose connection issues with your Railway bot
"""

import requests
import json
import sys

def test_bot_connection(bot_url):
    """Test all bot endpoints and report status"""
    
    print("🔍 Testing Bot Connection")
    print("=" * 50)
    print(f"Bot URL: {bot_url}")
    print()
    
    # Remove trailing slash
    bot_url = bot_url.rstrip('/')
    
    # Test 1: Health Check
    print("1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{bot_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health Check: PASSED")
            print(f"   Status: {health_data.get('status', 'unknown')}")
            print(f"   Webhook Ready: {health_data.get('webhook_ready', False)}")
            print(f"   Bot Initialized: {health_data.get('bot_initialized', False)}")
        else:
            print(f"❌ Health Check: FAILED (HTTP {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health Check: CONNECTION FAILED")
        print(f"   Error: {str(e)}")
        return False
    
    print()
    
    # Test 2: Status Check
    print("2️⃣ Testing Status Endpoint...")
    try:
        response = requests.get(f"{bot_url}/status", timeout=10)
        if response.status_code == 200:
            status_data = response.json()
            print("✅ Status Check: PASSED")
            print(f"   Mode: {status_data.get('mode', 'unknown')}")
            print(f"   Running: {status_data.get('running', False)}")
            print(f"   Total Trades: {status_data.get('total_trades', 0)}")
            if 'paper_balance' in status_data:
                print(f"   Paper Balance: ${status_data['paper_balance']:.2f}")
        else:
            print(f"❌ Status Check: FAILED (HTTP {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Status Check: CONNECTION FAILED")
        print(f"   Error: {str(e)}")
    
    print()
    
    # Test 3: Webhook Test
    print("3️⃣ Testing Webhook Endpoint...")
    test_signal = {
        "action": "BUY",
        "symbol": "BTCUSDT",
        "price": "50000",
        "strategy": "DIAGNOSTIC_TEST"
    }
    
    try:
        response = requests.post(
            f"{bot_url}/webhook",
            json=test_signal,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        if response.status_code == 200:
            webhook_data = response.json()
            print("✅ Webhook Test: PASSED")
            print(f"   Response: {webhook_data}")
        else:
            print(f"❌ Webhook Test: FAILED (HTTP {response.status_code})")
            print(f"   Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Webhook Test: CONNECTION FAILED")
        print(f"   Error: {str(e)}")
    
    print()
    return True

def main():
    print("🤖 Trading Bot Diagnostic Tool")
    print("=" * 50)
    
    # Get bot URL from user
    if len(sys.argv) > 1:
        bot_url = sys.argv[1]
    else:
        bot_url = input("Enter your Railway bot URL: ").strip()
    
    if not bot_url:
        print("❌ No URL provided. Exiting.")
        return
    
    # Add https:// if missing
    if not bot_url.startswith(('http://', 'https://')):
        bot_url = 'https://' + bot_url
    
    print(f"Testing bot at: {bot_url}")
    print()
    
    # Run tests
    success = test_bot_connection(bot_url)
    
    print("=" * 50)
    if success:
        print("🎉 Bot is responding! Connection successful.")
        print()
        print("📋 Next Steps:")
        print("1. Update your dashboard BOT_URL environment variable")
        print("2. Use this URL in your MT5 EA webhook setting")
        print("3. Test the complete system")
    else:
        print("🚨 Bot connection failed!")
        print()
        print("🔧 Troubleshooting:")
        print("1. Check if your Railway bot is deployed and running")
        print("2. Verify the URL is correct (should end with .railway.app)")
        print("3. Check Railway logs for any errors")
        print("4. Try redeploying your bot on Railway")
    
    print()
    print("📖 For more help, see TROUBLESHOOTING.md")

if __name__ == "__main__":
    main()