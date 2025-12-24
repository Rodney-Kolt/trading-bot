#!/usr/bin/env python3
"""
Switch to Profitable Trading System
This script switches the deployment from the basic system to the profitable system
"""

import shutil
import os
import sys

def switch_to_profitable():
    """Switch the system to use profitable components"""
    
    print("🔄 Switching to Profitable Trading System...")
    
    try:
        # Backup current files
        print("📦 Creating backups...")
        if os.path.exists('app.py'):
            shutil.copy2('app.py', 'app_basic.py.backup')
            print("✅ Backed up app.py → app_basic.py.backup")
        
        if os.path.exists('bot.py'):
            shutil.copy2('bot.py', 'bot_basic.py.backup')
            print("✅ Backed up bot.py → bot_basic.py.backup")
        
        # Switch to profitable versions
        print("🚀 Switching to profitable system...")
        
        if os.path.exists('profitable_app.py'):
            shutil.copy2('profitable_app.py', 'app.py')
            print("✅ Switched app.py → profitable_app.py")
        else:
            print("❌ profitable_app.py not found!")
            return False
        
        if os.path.exists('profitable_bot.py'):
            shutil.copy2('profitable_bot.py', 'bot.py')
            print("✅ Switched bot.py → profitable_bot.py")
        else:
            print("❌ profitable_bot.py not found!")
            return False
        
        # Switch dashboard
        dashboard_path = 'dashboard/streamlit_app.py'
        profitable_dashboard_path = 'dashboard/profitable_dashboard.py'
        
        if os.path.exists(profitable_dashboard_path):
            if os.path.exists(dashboard_path):
                shutil.copy2(dashboard_path, 'dashboard/streamlit_app_basic.py.backup')
                print("✅ Backed up dashboard → streamlit_app_basic.py.backup")
            
            shutil.copy2(profitable_dashboard_path, dashboard_path)
            print("✅ Switched dashboard → profitable_dashboard.py")
        
        print("\n🎯 System switched to Profitable Trading System!")
        print("📊 Features enabled:")
        print("   • Automation phases (Signal Only → Semi-Auto → Full Auto)")
        print("   • Enhanced risk management (0.5% risk per trade)")
        print("   • Profit tracking and withdrawal recommendations")
        print("   • Emergency stop controls")
        print("   • Session-based trading (London/NY)")
        print("   • Daily loss limits (2% max)")
        
        print("\n🚀 Next steps:")
        print("   1. Commit and push changes to GitHub")
        print("   2. Railway will auto-deploy the new system")
        print("   3. Update dashboard deployment")
        print("   4. Compile ProfitableEA.mq5 in MT5")
        print("   5. Test the complete system")
        
        return True
        
    except Exception as e:
        print(f"❌ Error switching system: {str(e)}")
        return False

def switch_back_to_basic():
    """Switch back to basic system"""
    
    print("🔄 Switching back to Basic Trading System...")
    
    try:
        # Restore from backups
        if os.path.exists('app_basic.py.backup'):
            shutil.copy2('app_basic.py.backup', 'app.py')
            print("✅ Restored app.py from backup")
        
        if os.path.exists('bot_basic.py.backup'):
            shutil.copy2('bot_basic.py.backup', 'bot.py')
            print("✅ Restored bot.py from backup")
        
        if os.path.exists('dashboard/streamlit_app_basic.py.backup'):
            shutil.copy2('dashboard/streamlit_app_basic.py.backup', 'dashboard/streamlit_app.py')
            print("✅ Restored dashboard from backup")
        
        print("\n✅ System switched back to Basic Trading System")
        return True
        
    except Exception as e:
        print(f"❌ Error switching back: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--back":
        switch_back_to_basic()
    else:
        switch_to_profitable()