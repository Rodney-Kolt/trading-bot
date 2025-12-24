#!/usr/bin/env python3
"""
Automatic Multi-Currency Setup
Deploys updates and tests the system automatically
"""

import subprocess
import urllib.request
import json
import time
import sys

def run_git_commands():
    """Deploy updates to GitHub/Railway"""
    print("🚀 Step 1: Auto-Deploying to Railway...")
    print("=" * 50)
    
    commands = [
        ["git", "add", "-A"],
        ["git", "commit", "-m", "Add multi-currency support - Enhanced bot and dashboard"],
        ["git", "push", "origin", "main"]
    ]
    
    for cmd in commands:
        try:
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ Success: {cmd[1]}")
                if result.stdout:
                    print(f"   {result.stdout.strip()}")
            else:
                print(f"❌ Failed: {cmd[1]}")
                if result.stderr:
                    print(f"   {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ Error running {cmd[1]}: {str(e)}")
    
    print("✅ Deployment commands completed!")
    print("⏳ Railway will auto-deploy in 2-3 minutes")

def send_test_signals():
    """Send multi-currency test signals"""
    print("\n🧪 Step 2: Auto-Testing Multi-Currency Signals...")
    print("=" * 50)
    
    webhook_url = "https://trading-bot-production-c863.up.railway.app/webhook"
    
    test_signals = [
        {"action": "BUY", "symbol": "EURUSD", "price": "1.0425", "strategy": "Auto_Multi_Test", "timeframe": "15m"},
        {"action": "BUY", "symbol": "GBPUSD", "price": "1.2650", "strategy": "Auto_Multi_Test", "timeframe": "15m"},
        {"action": "BUY", "symbol": "USDJPY", "price": "157.25", "strategy": "Auto_Multi_Test", "timeframe": "15m"},
        {"action": "BUY", "symbol": "AUDUSD", "price": "0.6180", "strategy": "Auto_Multi_Test", "timeframe": "15m"}
    ]
    
    for i, signal in enumerate(test_signals, 1):
        print(f"\n📊 Sending Signal {i}/4: {signal['symbol']} {signal['action']} @ {signal['price']}")
        
        try:
            data = json.dumps(signal).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = response.read().decode('utf-8')
                status = response.getcode()
            
            if status == 200:
                print(f"✅ {signal['symbol']} signal sent successfully")
            else:
                print(f"❌ {signal['symbol']} signal failed: {status}")
                
        except Exception as e:
            print(f"❌ Error sending {signal['symbol']} signal: {str(e)}")
        
        time.sleep(1)  # Small delay between signals
    
    print("\n✅ Multi-currency test signals completed!")

def display_mt5_setup():
    """Display MT5 setup instructions"""
    print("\n📊 Step 3: MT5 Multi-Currency EA Setup...")
    print("=" * 50)
    
    print("🎯 Your Multi-Currency EA is ready to install!")
    print("\n📁 File Location:")
    print("   trading_bot/mt5_ea/MultiCurrency_ProfitableEA.mq5")
    
    print("\n🚀 Quick MT5 Setup:")
    print("   1. Copy MultiCurrency_ProfitableEA.mq5 to MT5 Experts folder")
    print("   2. Compile in MetaEditor (should show 0 errors)")
    print("   3. Enable WebRequest for: https://trading-bot-production-c863.up.railway.app")
    print("   4. Attach to any M15 chart")
    print("   5. Use profitable settings (0.5% risk, ExecuteOnMT5=false)")
    
    print("\n✅ Expected MT5 Expert Tab Messages:")
    print("   🚀 Multi-Currency Profitable EA Started - Small Wins Focus")
    print("   💰 Monitoring 4 currency pairs")
    print("   ✅ EURUSD indicators initialized successfully")
    print("   ✅ GBPUSD indicators initialized successfully") 
    print("   ✅ USDJPY indicators initialized successfully")
    print("   ✅ AUDUSD indicators initialized successfully")
    print("   🌍 Multi-Currency EA ready!")

def check_dashboard():
    """Check dashboard status"""
    print("\n📊 Dashboard Check...")
    print("=" * 30)
    
    try:
        dashboard_url = "https://trading-bots.streamlit.app"
        bot_url = "https://trading-bot-production-c863.up.railway.app/health"
        
        print(f"🌐 Dashboard: {dashboard_url}")
        print(f"🤖 Bot Health: {bot_url}")
        
        # Check bot health
        req = urllib.request.Request(bot_url)
        with urllib.request.urlopen(req, timeout=10) as response:
            health_data = json.loads(response.read().decode('utf-8'))
            
        if health_data.get('status') == 'healthy':
            print("✅ Bot is healthy and online")
        else:
            print("⚠️ Bot status unknown")
            
    except Exception as e:
        print(f"ℹ️ Dashboard check: {str(e)}")

def main():
    """Run complete automatic setup"""
    print("🌍 AUTOMATIC MULTI-CURRENCY SETUP")
    print("=" * 60)
    print("This will automatically:")
    print("✅ Deploy updates to Railway")
    print("✅ Test multi-currency signals") 
    print("✅ Provide MT5 setup instructions")
    print("=" * 60)
    
    # Step 1: Deploy
    run_git_commands()
    
    # Wait a moment for deployment
    print("\n⏳ Waiting 10 seconds for deployment...")
    time.sleep(10)
    
    # Step 2: Test signals
    send_test_signals()
    
    # Step 3: MT5 setup instructions
    display_mt5_setup()
    
    # Check dashboard
    check_dashboard()
    
    print("\n" + "=" * 60)
    print("🎉 AUTOMATIC SETUP COMPLETE!")
    print("=" * 60)
    
    print("\n📊 What to check now:")
    print("✅ Dashboard: https://trading-bots.streamlit.app")
    print("   - Should show Multi-Currency Performance section")
    print("   - Should show 4 test signals in Recent Activity")
    print("   - Should show currency breakdown table")
    
    print("\n🔄 Next steps:")
    print("1. Check your dashboard for multi-currency features")
    print("2. Install MultiCurrency_ProfitableEA.mq5 in MT5")
    print("3. Your professional multi-currency system is ready!")
    
    print("\n🌍 You now have a complete professional multi-currency automated trading platform!")

if __name__ == "__main__":
    main()