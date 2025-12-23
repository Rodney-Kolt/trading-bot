#!/usr/bin/env python3
"""
Quick Git Setup Script for Trading Bot
Run this to initialize git and get ready for GitHub
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {str(e)}")
        return False
    return True

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("🚀 Trading Bot - Git Setup Script")
    print("=" * 40)
    
    # Check if git is installed
    if not check_git_installed():
        print("❌ Git is not installed. Please install Git first:")
        print("   Windows: https://git-scm.com/download/win")
        print("   Mac: brew install git")
        print("   Linux: sudo apt install git")
        sys.exit(1)
    
    print("✅ Git is installed")
    
    # Check if we're in the right directory
    required_files = ['app.py', 'bot.py', 'config.py', 'requirements.txt']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        print("   Make sure you're in the trading_bot directory")
        sys.exit(1)
    
    print("✅ All required files found")
    
    # Check if .env exists (should not be committed)
    if os.path.exists('.env'):
        print("⚠️  Found .env file - this will be ignored by git (good!)")
    
    # Initialize git repository
    if not os.path.exists('.git'):
        if not run_command('git init', 'Initializing git repository'):
            sys.exit(1)
    else:
        print("✅ Git repository already initialized")
    
    # Configure git user (if not set)
    result = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
    if not result.stdout.strip():
        name = input("Enter your name for git commits: ")
        run_command(f'git config user.name "{name}"', 'Setting git user name')
    
    result = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)
    if not result.stdout.strip():
        email = input("Enter your email for git commits: ")
        run_command(f'git config user.email "{email}"', 'Setting git user email')
    
    # Add files to git
    if not run_command('git add .', 'Adding files to git'):
        sys.exit(1)
    
    # Check git status
    run_command('git status', 'Checking git status')
    
    # Create initial commit
    commit_msg = "Initial commit: Complete trading bot with EMA+RSI strategy"
    if not run_command(f'git commit -m "{commit_msg}"', 'Creating initial commit'):
        print("ℹ️  Note: If no changes to commit, that's normal for subsequent runs")
    
    print("\n🎉 Git setup completed!")
    print("\n📋 Next steps:")
    print("1. Create a new repository on GitHub.com")
    print("2. Copy the repository URL")
    print("3. Run these commands:")
    print("   git remote add origin https://github.com/YOURUSERNAME/trading-bot.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\n📖 For detailed instructions, see GITHUB_SETUP.md")

if __name__ == "__main__":
    main()