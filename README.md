# Trading Bot 🤖📈

A complete Python trading bot that receives TradingView alerts and executes trades automatically with built-in risk management.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

> ⚠️ **Disclaimer**: This bot is for educational purposes. Trading involves substantial risk of loss. Always test thoroughly before live trading.

## 🚀 Features

✅ **Webhook Receiver** - Accepts TradingView alerts  
✅ **Risk Management** - Stop loss, position sizing, daily limits  
✅ **Trade Execution** - Automatic BUY/SELL orders  
✅ **Logging & Monitoring** - Complete trade history  
✅ **Safety First** - Multiple protection layers  

## 📁 Project Structure

```
trading_bot/
├── app.py              # Flask webhook server
├── bot.py              # Core trading logic
├── risk.py             # Risk management system
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

### 3. Configure Exchange API
- Create Binance API key (or your preferred exchange)
- Enable spot trading, disable withdrawals
- Add keys to `.env` file

### 4. Run the Bot
```bash
python app.py
```

Bot will start on `http://localhost:5000`

## 🔧 Configuration

Edit `.env` file with your settings:

### Exchange Settings
```env
API_KEY=your_binance_api_key
API_SECRET=your_binance_secret
SANDBOX_MODE=True  # Use testnet first!
```

### Risk Management 🛡️
```env
RISK_PERCENT=1.0           # Risk 1% per trade
STOP_LOSS_PERCENT=2.0      # 2% stop loss
TAKE_PROFIT_PERCENT=4.0    # 4% take profit
MAX_DAILY_LOSS=50.0        # Max $50 loss per day
MAX_CONSECUTIVE_LOSSES=3   # Stop after 3 losses
```

## 📡 TradingView Setup

### 1. Create Alert
- Open TradingView chart
- Add your strategy/indicators
- Create alert with webhook

### 2. Webhook URL
```
http://your-server.com/webhook
```

### 3. Alert Message (JSON)
```json
{
  "action": "{{strategy.order.action}}",
  "symbol": "{{ticker}}",
  "price": "{{close}}"
}
```

## 🛡️ Safety Features

### Risk Management
- **Position Sizing**: Risk only 1-2% per trade
- **Stop Loss**: Automatic 2% stop loss
- **Daily Limits**: Max loss and trade limits
- **Cooldown**: Prevents spam trading
- **Emergency Stop**: Manual override

### Validation
- Signal validation before execution
- Exchange connection monitoring
- Complete trade logging
- Error handling and recovery

## 📊 API Endpoints

### Webhook (POST /webhook)
Receives TradingView alerts
```json
{
  "action": "BUY",
  "symbol": "BTCUSDT", 
  "price": "50000"
}
```

### Status (GET /status)
Returns bot status and recent trades

### Health (GET /health)
Health check endpoint

## 🚨 Important Notes

### Before Going Live:
1. ✅ Test in sandbox mode first
2. ✅ Start with small amounts
3. ✅ Monitor logs carefully
4. ✅ Verify all risk settings
5. ✅ Have emergency stop ready

### Security:
- Never share API keys
- Use IP restrictions on exchange
- Disable withdrawals on API
- Keep logs secure

## 🔍 Monitoring

### Logs
Bot creates `trading_bot.log` with all activity:
- Incoming signals
- Trade executions
- Risk decisions
- Errors and warnings

### Status Endpoint
Check `/status` for:
- Current positions
- Recent trades
- Account balance
- Bot health

## 🛠️ Deployment

### Railway (Recommended)
1. Connect GitHub repo
2. Add environment variables
3. Deploy automatically

### Manual Server
1. Upload files to VPS
2. Install Python dependencies
3. Configure reverse proxy
4. Start with process manager

## ⚠️ Disclaimer

This bot is for educational purposes. Trading involves risk of loss. Always:
- Test thoroughly before live trading
- Start with small amounts
- Monitor performance closely
- Understand the risks involved

**Trade responsibly!** 📈🛡️

## 🚀 Quick Deploy

### Deploy to Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Click the Railway button above
2. Connect your GitHub account
3. Fork this repository
4. Add your environment variables
5. Deploy automatically

### Manual Setup
```bash
git clone https://github.com/yourusername/trading-bot.git
cd trading-bot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python app.py
```

## 📊 Strategy Performance

The included EMA + RSI strategy targets:
- **Win Rate**: 45-55%
- **Risk/Reward**: 2:1 (2% stop loss, 4% take profit)
- **Max Drawdown**: <15%
- **Timeframe**: 15m or 1h

## 🔗 Related Files

- [`strategy.pine`](strategy.pine) - TradingView Pine Script strategy
- [`STRATEGY_SETUP.md`](STRATEGY_SETUP.md) - Complete setup guide
- [`.env.example`](.env.example) - Environment variables template

## 📈 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Risk Warning

**IMPORTANT**: This software is provided for educational purposes only. Trading cryptocurrencies and other financial instruments involves substantial risk of loss and is not suitable for all investors. Past performance is not indicative of future results. You should carefully consider whether trading is suitable for you in light of your circumstances, knowledge, and financial resources.

The authors and contributors of this software:
- Do not guarantee profits or success
- Are not responsible for any losses incurred
- Recommend thorough testing before live trading
- Advise starting with small amounts
- Suggest consulting with financial advisors

**Always trade responsibly and never risk more than you can afford to lose.**