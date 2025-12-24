@echo off
echo 🚀 Sending Test Signal to Your Trading System...
echo.

curl -X POST ^
  -H "Content-Type: application/json" ^
  -d "{\"action\":\"BUY\",\"symbol\":\"EURUSD\",\"price\":\"1.0425\",\"strategy\":\"Test_Signal\",\"timeframe\":\"15m\"}" ^
  https://trading-bot-production-c863.up.railway.app/webhook

echo.
echo.
echo 🎉 Test signal sent!
echo 📊 Now check your dashboard - you should see:
echo    ✅ Daily Trades: 1
echo    ✅ Recent Activity: BUY signal received
echo.
pause