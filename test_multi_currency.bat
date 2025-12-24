@echo off
echo 🌍 Testing Multi-Currency Trading System...
echo.

echo 📊 Sending EURUSD BUY signal...
curl -X POST -H "Content-Type: application/json" -d "{\"action\":\"BUY\",\"symbol\":\"EURUSD\",\"price\":\"1.0425\",\"strategy\":\"Multi_Test\",\"timeframe\":\"15m\"}" https://trading-bot-production-c863.up.railway.app/webhook

echo.
echo 📊 Sending GBPUSD BUY signal...
curl -X POST -H "Content-Type: application/json" -d "{\"action\":\"BUY\",\"symbol\":\"GBPUSD\",\"price\":\"1.2650\",\"strategy\":\"Multi_Test\",\"timeframe\":\"15m\"}" https://trading-bot-production-c863.up.railway.app/webhook

echo.
echo 📊 Sending USDJPY BUY signal...
curl -X POST -H "Content-Type: application/json" -d "{\"action\":\"BUY\",\"symbol\":\"USDJPY\",\"price\":\"157.25\",\"strategy\":\"Multi_Test\",\"timeframe\":\"15m\"}" https://trading-bot-production-c863.up.railway.app/webhook

echo.
echo 📊 Sending AUDUSD BUY signal...
curl -X POST -H "Content-Type: application/json" -d "{\"action\":\"BUY\",\"symbol\":\"AUDUSD\",\"price\":\"0.6180\",\"strategy\":\"Multi_Test\",\"timeframe\":\"15m\"}" https://trading-bot-production-c863.up.railway.app/webhook

echo.
echo 🎉 Multi-currency test signals sent!
echo 📊 Check your dashboard - you should see:
echo    ✅ Daily Trades: 4
echo    ✅ Recent Activity: Multiple currency signals
echo    ✅ EURUSD, GBPUSD, USDJPY, AUDUSD signals
echo.
pause