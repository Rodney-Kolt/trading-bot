# 🚀 Complete Deployment Guide

Your trading bot is ready! Follow these steps to get it live on GitHub and Railway.

## 📋 Step 1: Create GitHub Repository

1. **Go to GitHub:**
   - Open [github.com](https://github.com) in your browser
   - Sign in to your account (or create one if needed)

2. **Create New Repository:**
   - Click the green "New" button (or "+" icon → "New repository")
   - Repository name: `trading-bot`
   - Description: `Automated trading bot with TradingView integration and risk management`
   - Set to **Public** (recommended for Railway deployment)
   - **DO NOT** check "Add a README file" (we already have one)
   - **DO NOT** check "Add .gitignore" (we already have one)
   - Click "Create repository"

3. **Copy the Repository URL:**
   - After creation, you'll see commands like this:
   ```
   git remote add origin https://github.com/YOURUSERNAME/trading-bot.git
   ```
   - Copy your actual URL (replace YOURUSERNAME with your GitHub username)

## 📤 Step 2: Push to GitHub

Open your terminal in the `trading_bot` folder and run:

```bash
# Add GitHub as remote (replace YOURUSERNAME with your actual username)
git remote add origin https://github.com/YOURUSERNAME/trading-bot.git

# Push to GitHub
git push -u origin main
```

**Expected result:** All your files will upload to GitHub (except .env which is safely ignored).

## 🚀 Step 3: Deploy to Railway

1. **Go to Railway:**
   - Open [railway.app](https://railway.app)
   - Click "Login" and sign in with GitHub

2. **Deploy from GitHub:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `trading-bot` repository
   - Click "Deploy Now"

3. **Add Environment Variables:**
   After deployment starts, click on your project, then "Variables" tab:

   ```env
   API_KEY=your_binance_api_key_here
   API_SECRET=your_binance_secret_here
   SANDBOX_MODE=true
   ACCOUNT_BALANCE=1000
   RISK_PERCENT=1.0
   STOP_LOSS_PERCENT=2.0
   TAKE_PROFIT_PERCENT=4.0
   MAX_DAILY_LOSS=50.0
   PORT=5000
   ```

4. **Get Your Webhook URL:**
   - After deployment, Railway will give you a URL like:
   - `https://your-app-name.railway.app`
   - Your webhook endpoint will be:
   - `https://your-app-name.railway.app/webhook`

## 🔧 Step 4: Test Your Deployment

1. **Check if bot is running:**
   - Visit: `https://your-app-name.railway.app/health`
   - Should return: `{"status": "healthy", ...}`

2. **Test webhook:**
   - Use the test script or send a POST request to `/webhook`

## 📡 Step 5: Connect TradingView

1. **Add Pine Script Strategy:**
   - Copy the code from `strategy.pine`
   - Add to TradingView Pine Editor
   - Apply to BTCUSDT 15m chart

2. **Create Alert:**
   - Right-click chart → "Add Alert"
   - Condition: Your strategy name
   - Webhook URL: `https://your-app-name.railway.app/webhook`
   - Message: (already configured in Pine Script)

3. **Test Alert:**
   - Trigger a test alert
   - Check Railway logs for incoming signals

## 🛡️ Step 6: Safety Checklist

Before going live:

- [ ] Bot deployed and running on Railway
- [ ] Environment variables set correctly
- [ ] `SANDBOX_MODE=true` for testing
- [ ] Webhook receiving test signals
- [ ] TradingView alerts configured
- [ ] Binance API keys have correct permissions
- [ ] API keys have withdrawals DISABLED
- [ ] Start with small `ACCOUNT_BALANCE`

## 📊 Step 7: Monitor Performance

**Daily Checks:**
- Railway app logs
- Bot status endpoint
- Trade history
- P&L tracking
- Error monitoring

**Weekly Reviews:**
- Strategy performance
- Risk metrics
- Drawdown analysis
- Win rate tracking

## 🚨 Troubleshooting

### Common Issues:

**Bot won't start:**
- Check Railway logs for errors
- Verify all environment variables are set
- Ensure API keys are valid

**Webhook not receiving signals:**
- Check TradingView alert URL
- Verify Railway app is running
- Test with `/health` endpoint

**Trades not executing:**
- Check API key permissions
- Verify symbol is supported
- Check risk management logs

### Getting Help:

1. Check Railway deployment logs
2. Review bot logs in Railway console
3. Test individual components
4. Verify all configurations

## 🎯 Success Metrics

Your bot is working correctly when:

✅ Railway deployment shows "Active"  
✅ Health endpoint returns 200 OK  
✅ Webhook receives TradingView signals  
✅ Risk management blocks invalid trades  
✅ Valid trades execute on exchange  
✅ All trades are logged properly  

## 🔄 Making Updates

To update your bot:

1. Make changes to your local files
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: describe your changes"
   git push origin main
   ```
3. Railway will automatically redeploy

## 💰 Going Live

When ready for real trading:

1. Change `SANDBOX_MODE=false`
2. Update `ACCOUNT_BALANCE` to real amount
3. Start with small position sizes
4. Monitor closely for first week
5. Gradually increase if performing well

**Remember: Start small, test thoroughly, and never risk more than you can afford to lose!**