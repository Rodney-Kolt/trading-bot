@echo off
echo 🌍 Quick Multi-Currency Test...
echo.

echo Sending EURUSD signal...
curl -s -X POST -H "Content-Type: application/json" -d "{\"action\":\"BUY\",\"symbol\":\"EURUSD\",\"price\":\"1.0425\",\"strategy\":\"Multi_Test\"}" https://trading-bot-production-c863.up.railway.app/webhook

echo.
echo Sending GBPUSD signal...
curl -s -X POST -H "Content-Type: application/json" -d "{\"action\":\"BUY\",\"symbol\":\"GBPUSD\",\"price\":\"1.2650\",\"strategy\":\"Multi_Test\"}" https://trading-bot-production-c863.up.railway.app/webhook

echo.
echo 🎉 Multi-currency signals sent!
echo 📊 Check your dashboard now!
pause