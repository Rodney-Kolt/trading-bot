#!/usr/bin/env python3
"""
Deploy Multi-Currency System
Updates the system files and commits to GitHub for auto-deployment
"""

import subprocess
import sys

def run_command(command, description):
    """Run a command and handle the result"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} error: {str(e)}")
        return False

def deploy_multi_currency():
    """Deploy the multi-currency system"""
    
    print("🌍 Deploying Multi-Currency Trading System...")
    print("=" * 60)
    
    # Git commands
    commands = [
        ("git add .", "Adding files to git"),
        ('git commit -m "Add multi-currency support - Enhanced bot and dashboard"', "Committing changes"),
        ("git push origin main", "Pushing to GitHub")
    ]
    
    success = True
    for command, description in commands:
        if not run_command(command, description):
            success = False
            break
    
    if success:
        print("\n🎉 Multi-Currency System Deployed Successfully!")
        print("\n📊 What's New:")
        print("   ✅ Multi-Currency EA (monitors 4 pairs simultaneously)")
        print("   ✅ Enhanced Python Bot (tracks each currency separately)")
        print("   ✅ Updated Dashboard (currency breakdown & performance)")
        print("   ✅ Test Scripts (multi-currency signal testing)")
        
        print("\n🚀 Next Steps:")
        print("   1. Wait for Railway auto-deployment (2-3 minutes)")
        print("   2. Use MultiCurrency_ProfitableEA.mq5 in MT5")
        print("   3. Test with test_multi_system.py")
        print("   4. Check dashboard for multi-currency display")
        
        print("\n🌍 Your system now supports:")
        print("   • EURUSD, GBPUSD, USDJPY, AUDUSD")
        print("   • Individual currency performance tracking")
        print("   • Multi-currency risk management")
        print("   • Enhanced dashboard with currency breakdown")
        
    else:
        print("\n❌ Deployment failed!")
        print("🔧 Try running the git commands manually")

if __name__ == "__main__":
    deploy_multi_currency()