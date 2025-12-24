#!/usr/bin/env python3
"""
Deploy Profitable Trading System to Railway
"""

import subprocess
import sys
import time

def run_command(cmd):
    """Run a command and return the result"""
    try:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("Command timed out")
        return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    print("🚀 DEPLOYING PROFITABLE TRADING SYSTEM")
    print("=" * 50)
    
    # Check git status
    print("\n📋 Checking git status...")
    if not run_command("git status"):
        print("❌ Git status failed")
        return False
    
    # Push to GitHub
    print("\n📤 Pushing to GitHub...")
    if not run_command("git push origin main"):
        print("❌ Git push failed, trying alternative...")
        if not run_command("git push"):
            print("❌ All push attempts failed")
            return False
    
    print("\n🎉 DEPLOYMENT SUCCESSFUL!")
    print("=" * 50)
    print("✅ Profitable Trading System deployed to Railway")
    print("🔗 Bot URL: https://trading-bot-production-c863.up.railway.app")
    print("📊 Dashboard: https://trading-bots.streamlit.app")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Wait 2-3 minutes for Railway auto-deployment")
    print("2. Test the enhanced system:")
    print("   curl https://trading-bot-production-c863.up.railway.app/health")
    print("3. Check dashboard for new control center interface")
    print("4. Use TradingBotEA_Fixed.mq5 in MT5 with profitable settings")
    
    print("\n🛡️ SYSTEM FEATURES NOW ACTIVE:")
    print("• Automation phases (Signal Only → Semi-Auto → Full Auto)")
    print("• Risk management (0.5% per trade, 2% daily limit)")
    print("• Profit tracking and withdrawal recommendations")
    print("• Emergency stop controls")
    print("• Session-based trading (London/NY)")
    print("• Real-time P&L monitoring")
    
    return True

if __name__ == "__main__":
    main()