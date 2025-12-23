# 📊 TradingView-Only Setup Guide

**Perfect for testing strategies without any exchange connection!**

Your bot can now work with **TradingView only** - no Binance, no API keys, no geographic restrictions. Just pure strategy testing and signal tracking.

## 🎯 What This Mode Does

✅ **Receives TradingView alerts** via webhook  
✅ **Simulates trades** with virtual money  
✅ **Tracks performance** (P&L, win rate, etc.)  
✅ **Applies risk management** (stop loss, position sizing)  
✅ **Logs everything** for analysis  
❌ **No real money** - completely safe  
❌ **No exchange needed** - works anywhere  

## 🚀 Quick Setup

### Step 1: Deploy with TradingView-Only Mode

In Railway, set these environment variables:

```env
TRADINGVIEW_ONLY=true
EXCHANGE=none
ACCOUNT_BALANCE=1000
RISK_PERCENT=1.0
STOP_LOSS_PERCENT=2.0
TAKE_PROFIT_PERCENT=4.0
```

**No API keys needed!** 🎉

### Step 2: Get Your Webhook URL

After Railway deployment:
- Your webhook URL: `https://your-app.railway.app/webhook`
- Health check: `https://your-app.railway.app/health`
- Status page: `https://your-app.railway.app/status`

### Step 3: Setup TradingView Strategy

1. **Add the Pine Script:**
   - Copy code from `strategy.pine`
   - Add to TradingView Pine Editor
   - Apply to BTCUSDT 15m chart

2. **Create Alert:**
   - Right-click chart → "Add Alert"
   - Condition: Your strategy
   - Webhook URL: `https://your-app.railway.app/webhook`
   - Message: (already configured in Pine Script)

### Step 4: Test Everything

Send a test webhook:
```bash
curl -X POST https://your-app.railway.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"action":"BUY","symbol":"BTCUSDT","price":"50000"}'
```

## 📊 What You'll See

### Bot Status Page
Visit `https://your-app.railway.app/status` to see:

```json
{
  "running": true,
  "mode": "TradingView-only (Simulated)",
  "paper_balance": 1050.25,
  "starting_balance": 1000,
  "total_pnl": 50.25,
  "total_pnl_percent": 5.02,
  "positions": {
    "BTCUSDT": {
      "side": "long",
      "size": 0.02,
      "entry_price": 49500,
      "simulated": true
    }
  },
  "recent_trades": [...],
  "total_trades": 15
}
```

### Trade Logs
Every signal and trade is logged:

```
2024-12-23 18:30:15 - INFO - Processing BUY signal for BTCUSDT at 50000
2024-12-23 18:30:15 - INFO - SIMULATED BUY: BTCUSDT - Size: 0.02 - Price: $50000 - Value: $1000.00
2024-12-23 18:45:22 - INFO - Processing SELL signal for BTCUSDT at 52000  
2024-12-23 18:45:22 - INFO - SIMULATED SELL: BTCUSDT - P&L: $40.00 (4.00%) - Balance: $1040.00
```

## 🎯 Perfect For

### Strategy Testing
- Test Pine Script strategies risk-free
- See real performance metrics
- Optimize entry/exit rules
- Track win rates and drawdowns

### Learning
- Understand how trading bots work
- Practice with TradingView alerts
- Learn risk management
- No fear of losing money

### Development
- Test webhook integrations
- Debug bot logic
- Validate signal processing
- Perfect for beginners

## 📈 Performance Tracking

The bot tracks everything:

**Trade Metrics:**
- Total trades executed
- Win rate percentage
- Average profit/loss
- Maximum drawdown
- Sharpe ratio (coming soon)

**Risk Metrics:**
- Position sizes
- Stop loss triggers
- Daily loss limits
- Consecutive loss tracking

**Balance Tracking:**
- Starting balance: $1000
- Current balance: Updates with each trade
- Total P&L: Profit/loss since start
- P&L percentage: Return on investment

## 🔄 Upgrading to Live Trading

When you're ready for real trading:

1. **Change environment variables:**
```env
TRADINGVIEW_ONLY=false
EXCHANGE=binance
API_KEY=your_real_api_key
API_SECRET=your_real_secret
SANDBOX_MODE=true  # Start with testnet
```

2. **Test with small amounts**
3. **Monitor closely**
4. **Scale up gradually**

## 🛡️ Safety Features

Even in simulation mode, all safety features work:

✅ **Risk Management** - 1% risk per trade  
✅ **Stop Loss** - 2% automatic stop  
✅ **Daily Limits** - Max loss protection  
✅ **Position Limits** - Max 3 positions  
✅ **Cooldown** - Prevents spam trading  

## 🎉 Benefits

**No Exchange Needed:**
- Works anywhere in the world
- No API key setup
- No geographic restrictions
- No account verification

**Risk-Free Testing:**
- Virtual money only
- Test strategies safely
- Learn without fear
- Perfect for beginners

**Real Performance Data:**
- Accurate simulation
- Proper risk management
- Realistic trade execution
- Detailed logging

## 📞 Support

If you need help:
1. Check Railway logs for errors
2. Test webhook with curl command
3. Verify TradingView alert setup
4. Check bot status page

**This mode is perfect for learning and testing before going live with real money!** 🚀📊