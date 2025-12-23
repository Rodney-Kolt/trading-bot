# 🚀 GitHub Setup Guide

Follow these steps to get your trading bot on GitHub and ready for deployment.

## 📋 Prerequisites

- Git installed on your computer
- GitHub account created
- Trading bot files ready

## 🛠️ Step-by-Step Setup

### Step 1: Initialize Git Repository

Open terminal in your `trading_bot` folder and run:

```bash
# Initialize git repository
git init

# Add all files to staging
git add .

# Create first commit
git commit -m "Initial commit: Complete trading bot with EMA+RSI strategy"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "New Repository" (green button)
3. Repository name: `trading-bot` (or your preferred name)
4. Description: `Automated trading bot with TradingView integration`
5. Set to **Public** (or Private if you prefer)
6. **DO NOT** initialize with README (we already have one)
7. Click "Create Repository"

### Step 3: Connect Local Repository to GitHub

Copy the commands from GitHub (they'll look like this):

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/YOURUSERNAME/trading-bot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOURUSERNAME` with your actual GitHub username.

### Step 4: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. Check that `.env` is **NOT** visible (it should be ignored)

## 🔒 Security Checklist

Before pushing to GitHub, verify:

- [ ] `.env` file is in `.gitignore` ✅
- [ ] No API keys in any files ✅
- [ ] `.env.example` has placeholder values only ✅
- [ ] All sensitive data is excluded ✅

## 🚀 Deploy to Railway

Once on GitHub, you can deploy to Railway:

1. Go to [Railway.app](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select your `trading-bot` repository
4. Add environment variables:
   ```
   API_KEY=your_binance_api_key
   API_SECRET=your_binance_secret
   SANDBOX_MODE=true
   ACCOUNT_BALANCE=1000
   ```
5. Deploy automatically

## 📝 Repository Structure

Your GitHub repo will contain:

```
trading-bot/
├── .github/workflows/     # Automated testing
├── app.py                # Main Flask application
├── bot.py                # Trading logic
├── risk.py               # Risk management
├── config.py             # Configuration
├── strategy.pine         # TradingView strategy
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
├── README.md            # Documentation
├── LICENSE              # MIT license
└── STRATEGY_SETUP.md    # Strategy guide
```

## 🔄 Making Updates

After initial setup, to update your bot:

```bash
# Make your changes to files
# Then commit and push:

git add .
git commit -m "Update: describe your changes"
git push origin main
```

Railway will automatically redeploy when you push to GitHub.

## 🎯 Next Steps

1. ✅ Push to GitHub
2. ✅ Deploy to Railway
3. ✅ Add environment variables
4. ✅ Test webhook endpoint
5. ✅ Create TradingView alerts
6. ✅ Start paper trading

## 🆘 Troubleshooting

### Git Issues
```bash
# If you get authentication errors:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# If remote already exists:
git remote remove origin
git remote add origin https://github.com/YOURUSERNAME/trading-bot.git
```

### File Too Large
If you get file size errors:
```bash
# Check file sizes
ls -lh

# Remove large files and add to .gitignore
echo "large_file.log" >> .gitignore
git rm --cached large_file.log
```

### Sensitive Data Leaked
If you accidentally committed sensitive data:
```bash
# Remove from git history (DANGER - rewrites history)
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all

# Force push (only if repository is private and you're sure)
git push origin --force --all
```

## 📞 Support

If you run into issues:
1. Check the error message carefully
2. Verify all files are in the right place
3. Ensure `.env` is not being tracked
4. Make sure GitHub repository is created correctly

**Remember**: Never commit API keys or sensitive data to GitHub!