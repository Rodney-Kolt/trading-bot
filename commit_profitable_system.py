#!/usr/bin/env python3
"""
Commit the profitable system changes
"""

import subprocess
import sys

def run_command(cmd):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"Command: {cmd}")
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Exception running command: {e}")
        return False

def main():
    print("🔄 Committing profitable system changes...")
    
    # Add all changes
    if not run_command("git add ."):
        print("❌ Failed to add changes")
        return False
    
    # Commit changes
    commit_msg = "Switch to Profitable Trading System - Enhanced automation phases, risk management, and profit tracking"
    if not run_command(f'git commit -m "{commit_msg}"'):
        print("❌ Failed to commit changes")
        return False
    
    # Push changes
    if not run_command("git push origin main"):
        print("❌ Failed to push changes")
        return False
    
    print("✅ Successfully deployed profitable system!")
    print("🚀 Railway will auto-deploy the new system")
    print("📊 New features:")
    print("   • Automation phases (Signal Only → Semi-Auto → Full Auto)")
    print("   • Enhanced risk management (0.5% risk per trade)")
    print("   • Profit tracking and withdrawal recommendations")
    print("   • Emergency stop controls")
    print("   • Session-based trading (London/NY)")
    print("   • Daily loss limits (2% max)")
    
    return True

if __name__ == "__main__":
    main()