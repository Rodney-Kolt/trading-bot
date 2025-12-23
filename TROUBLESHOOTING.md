# 🔧 Troubleshooting Guide

## 🚨 Common Issues & Solutions

### Issue 1: Dashboard Shows "Bot Offline" / HTTP 404

**Symptoms:**
- Dashboard shows "🔴 Bot Offline"
- "📡 Webhook Not Ready"
- "❌ Cannot connect to bot: HTTP 404"

**Causes & Solutions:**

#### A) Railway Bot Not Running
1. **Check Railway Dashboard:**
   - Go to https://railway.app/dashboard
   - Find your trading bot project
   - Check if it shows "Active" or "Crashed"

2. **If Crashed, Check Logs:**
   - Click on your bot project
   - Go to "Deployments" tab
   - Click latest deployment
   - Check logs for errors

3. **Common Fixes:**
   - Redeploy: Click "Redeploy" button
   - Check environment variables are set
   - Verify `requirements.txt` is correct

#### B) Wrong Bot URL in Dashboard
1. **Get Correct Railway URL:**
   - In Railway project, go to "Settings" tab
   - Copy the "Public Domain" URL
   - Should look like: `https://trading-bot-production-xxxx.up.railway.app`

2. **Update Dashboard Environment Variable:**
   - In Railway dashboard (for your dashboard project)
   - Go to "Variables" tab
   - Set: `BOT_URL=https://your-correct-bot-url.railway.app`
   - Redeploy dashboard

#### C) Bot URL Format Issues
Make sure your bot URL:
- ✅ Starts with `https://`
- ✅ Ends with `.railway.app` (no trailing slash)
- ✅ Is the PUBLIC domain, not internal Railway URL

### Issue 2: MT5 EA Compilation Errors

**Common MQL5 Fixes:**

#### Error: "slowEMA" - variable not declared
**Fix:** Change line 15 to:
```mql5
double fastEMA[], slowEMA[], trendEMA[], rsi[];
```

#### Error: WebRequest not allowed
**Fix in MT5:**
1. Tools → Options → Expert Advisors
2. Check "Allow WebRequest for listed URL"
3. Add: `https://your-bot-url.railway.app`

#### Error: Indicators not initializing
**Fix:** Ensure you're using correct symbol and timeframe:
- Attach EA to EURUSD or GBPUSD chart
- Use M15 (15-minute) timeframe

### Issue 3: No Signals Generated

**Checklist:**
- ✅ EA attached to active chart
- ✅ Auto-trading enabled in MT5
- ✅ Market is open and moving
- ✅ EMA crossover conditions met
- ✅ 5-minute cooldown period passed

### Issue 4: Webhook Not Receiving Signals

**Debug Steps:**

1. **Test Bot Directly:**
   ```bash
   curl -X POST https://your-bot-url.railway.app/webhook \
     -H "Content-Type: application/json" \
     -d '{"action":"BUY","symbol":"EURUSD","price":"1.1000"}'
   ```

2. **Check Railway Logs:**
   - Should show: "Received signal: {...}"
   - If not, check bot is running

3. **Check MT5 EA Logs:**
   - Should show: "✅ Webhook sent successfully"
   - If shows error code, check URL and WebRequest settings

## 🛠️ Quick Diagnostic Commands

### Test Bot Health
```bash
curl https://your-bot-url.railway.app/health
```
**Expected Response:**
```json
{
  "status": "healthy",
  "webhook_ready": true,
  "bot_initialized": true
}
```

### Test Bot Status
```bash
curl https://your-bot-url.railway.app/status
```
**Expected Response:**
```json
{
  "running": true,
  "mode": "TradingView-only (Simulated)",
  "paper_balance": 1000.0
}
```

### Send Test Signal
```bash
curl -X POST https://your-bot-url.railway.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"action":"BUY","symbol":"BTCUSDT","price":"50000"}'
```

## 🔄 Step-by-Step Recovery

### If Everything is Broken:

1. **Check Railway Bot:**
   - Go to Railway dashboard
   - Verify bot project is "Active"
   - Check recent deployment logs
   - Redeploy if needed

2. **Get Correct URLs:**
   - Copy bot URL from Railway
   - Update dashboard `BOT_URL` variable
   - Redeploy dashboard

3. **Test Connections:**
   - Use curl commands above
   - Check dashboard connects to bot
   - Verify MT5 EA can send webhooks

4. **Verify MT5 Setup:**
   - Recompile EA in MetaEditor
   - Check WebRequest permissions
   - Attach to active chart with movement

## 📞 Getting Help

### Information to Collect:
1. **Railway Bot URL:** `https://your-bot.railway.app`
2. **Railway Bot Logs:** Copy recent error messages
3. **Dashboard URL:** `https://your-dashboard.railway.app`
4. **MT5 EA Status:** Check Expert tab for messages
5. **Test Results:** Output from curl commands

### Common Solutions Summary:
- **404 Errors:** Wrong URL or bot not running
- **Connection Refused:** Bot crashed or not deployed
- **Webhook Fails:** WebRequest not enabled in MT5
- **No Signals:** Market conditions or EA settings
- **Dashboard Empty:** Bot URL not set correctly

## ✅ Success Checklist

Your system is working when:
- ✅ `curl bot/health` returns "healthy"
- ✅ Dashboard shows "🟢 Bot Online"
- ✅ MT5 EA shows "Trading Bot EA Started"
- ✅ Test webhook returns success response
- ✅ Dashboard updates with test signals