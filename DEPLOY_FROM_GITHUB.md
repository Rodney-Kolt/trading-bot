# 🚀 Deploy Complete System from GitHub

**Using your existing repository: https://github.com/Rodney-Kolt/trading-bot**

Your GitHub repo now contains everything needed for the complete trading system. Here's how to deploy each component.

## 📋 What's in Your Repository

```
trading-bot/
├── app.py                    # Main Python bot (Flask server)
├── bot.py                    # Trading logic & simulation
├── risk.py                   # Risk management
├── config.py                 # Configuration
├── requirements.txt          # Python dependencies
├── dashboard/                # Streamlit dashboard
│   ├── streamlit_app.py     # Dashboard interface
│   ├── requirements.txt     # Dashboard dependencies
│   └── .streamlit/config.toml
├── mt5_ea/                   # MetaTrader 5 Expert Advisor
│   └── TradingBotEA.mq5     # MT5 signal generator
└── docs/                     # All setup guides
```

## 🎯 Deployment Plan

### Component 1: Python Bot (Already Done!)
✅ **Status:** Already deployed on Railway  
✅ **URL:** Your existing Railway app  
✅ **Function:** Receives webhooks, simulates trades, logs data  

### Component 2: Streamlit Dashboard (New Deployment)
🎯 **Deploy from same GitHub repo**  
🎯 **Function:** Live monitoring, charts, controls  

### Component 3: MT5 Expert Advisor (Local Setup)
🎯 **Download from GitHub**  
🎯 **Function:** Generate signals, send webhooks  

## 🚀 Step 1: Deploy Streamlit Dashboard

### Option A: Railway (Recommended)

1. **Go to Railway.app**
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose `Rodney-Kolt/trading-bot`** (your existing repo)
5. **IMPORTANT:** Set root directory to `dashboard`
   - In Railway project settings
   - Set "Root Directory" to `dashboard`
6. **Add environment variables:**
   ```env
   BOT_URL=https://your-existing-bot-app.railway.app
   ```
7. **Deploy**

Railway will automatically:
- Detect `dashboard/requirements.txt`
- Install Streamlit dependencies
- Run `streamlit run streamlit_app.py`
- Give you a dashboard URL

### Option B: Streamlit Cloud (Alternative)

1. **Go to share.streamlit.io**
2. **Connect GitHub account**
3. **Deploy from `Rodney-Kolt/trading-bot`**
4. **Set main file path:** `dashboard/streamlit_app.py`
5. **Add secrets in Streamlit Cloud:**
   ```toml
   BOT_URL = "https://your-bot-app.railway.app"
   ```

## 🎯 Step 2: Setup MT5 Expert Advisor

### Download EA from GitHub

1. **Go to your GitHub repo:** https://github.com/Rodney-Kolt/trading-bot
2. **Navigate to:** `mt5_ea/TradingBotEA.mq5`
3. **Click "Raw" and save file**
4. **Or clone entire repo:**
   ```bash
   git clone https://github.com/Rodney-Kolt/trading-bot.git
   ```

### Install in MT5

1. **Open MetaTrader 5**
2. **Copy `TradingBotEA.mq5` to:**
   - Windows: `C:\Users\[Username]\AppData\Roaming\MetaQuotes\Terminal\[ID]\MQL5\Experts\`
   - Mac: `~/Library/Application Support/MetaQuotes/Terminal/[ID]/MQL5/Experts/`
3. **Open MetaEditor (F4 in MT5)**
4. **Compile the EA (F7)**
5. **Drag EA to chart (EURUSD 15m recommended)**

### Configure EA Settings

When attaching EA to chart, set:
```
WebhookURL = "https://your-bot-app.railway.app/webhook"
FastEMA = 9
SlowEMA = 21
TrendEMA = 200
RSIPeriod = 14
RiskPercent = 1.0
StopLossPercent = 2.0
TakeProfitPercent = 4.0
SendWebhooks = true
ExecuteOnMT5 = true
```

### Enable WebRequest in MT5

1. **Tools → Options → Expert Advisors**
2. **Check "Allow WebRequest for listed URL"**
3. **Add your bot URL:** `https://your-bot-app.railway.app`
4. **Click OK**

## 🔗 Step 3: Connect Everything

### Your System URLs

After deployment, you'll have:

1. **Python Bot:** `https://your-bot-app.railway.app`
   - Webhook: `/webhook`
   - Status: `/status`
   - Health: `/health`

2. **Dashboard:** `https://your-dashboard-app.railway.app`
   - Live monitoring interface
   - Manual controls
   - Performance charts

3. **MT5 EA:** Running locally on your computer
   - Generates signals
   - Sends webhooks to Python bot
   - Executes demo trades

### Test the Complete System

1. **Check Python Bot:**
   ```bash
   curl https://your-bot-app.railway.app/health
   ```
   Should return: `{"status": "healthy", "webhook_ready": true}`

2. **Check Dashboard:**
   - Visit dashboard URL
   - Should show bot status and controls
   - Try sending test signals

3. **Check MT5 EA:**
   - Should show "Trading Bot EA Started" in MT5 logs
   - Watch for EMA crossovers on chart
   - Check webhook sends in MT5 Expert tab

## 📊 Step 4: Monitor Live System

### Dashboard Features

Your Streamlit dashboard will show:

- **🟢 Bot Status:** Online/Offline, Webhook Ready
- **📊 Performance:** Balance, Total Return, Trade Count
- **📍 Positions:** Current open trades
- **📈 Trade History:** Recent signals and results
- **📉 P&L Chart:** Cumulative performance over time
- **🧪 Test Controls:** Send manual BUY/SELL signals

### MT5 Monitoring

In MT5 you'll see:
- **Chart:** EMA lines and signal arrows
- **Expert Tab:** EA logs and webhook confirmations
- **Trade Tab:** Demo positions and P&L
- **Journal:** Connection and signal status

### Python Bot Logs

In Railway logs you'll see:
```
INFO - Trading Bot initialized in TradingView-only mode
INFO - Received signal: {"action":"BUY","symbol":"EURUSD","price":"1.1050"}
INFO - SIMULATED BUY: EURUSD - Size: 0.02 - Price: $1.1050
INFO - SIMULATED SELL: EURUSD - P&L: $15.50 (1.40%)
```

## 🎯 Expected Workflow

```
MT5 Chart (EURUSD 15m)
    ↓ EMA Crossover Detected
MT5 EA Generates Signal
    ↓ Webhook POST Request
Python Bot (Railway)
    ↓ Risk Check & Simulation
Dashboard Updates
    ↓ Live Monitoring
You See Results in Real-Time
```

## 🛠️ Troubleshooting

### Dashboard Won't Connect
- Check `BOT_URL` environment variable
- Verify Python bot is running
- Test bot health endpoint directly

### MT5 EA Not Sending Signals
- Check WebRequest is enabled
- Verify webhook URL is correct
- Look for compilation errors in MetaEditor

### No Signals Generated
- Ensure EA is attached to active chart
- Check EMA settings match market conditions
- Verify auto-trading is enabled in MT5

## 🎉 Success Indicators

Your system is working when:

✅ **Dashboard shows "Bot Online"**  
✅ **MT5 EA shows "Trading Bot EA Started"**  
✅ **Webhook signals appear in Railway logs**  
✅ **Dashboard updates with new trades**  
✅ **P&L tracking is accurate**  

## 📈 Next Steps

1. **Run system for 1 week** to collect performance data
2. **Optimize EA parameters** based on results
3. **Add more symbols** (BTCUSD, GBPUSD, etc.)
4. **Consider real trading** when confident in strategy

**Your complete trading system is now deployable from your GitHub repository!** 🚀

## 🔗 Quick Links

- **Your GitHub Repo:** https://github.com/Rodney-Kolt/trading-bot
- **Railway Dashboard:** https://railway.app/dashboard
- **Streamlit Cloud:** https://share.streamlit.io
- **Complete System Guide:** See `COMPLETE_SYSTEM_GUIDE.md` in your repo