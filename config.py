"""
Trading Bot Configuration
All settings and parameters in one place
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Server Settings
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Exchange Settings
    EXCHANGE = os.getenv('EXCHANGE', 'none')  # Set to 'none' for TradingView-only mode
    API_KEY = os.getenv('API_KEY', '')
    API_SECRET = os.getenv('API_SECRET', '')
    SANDBOX_MODE = os.getenv('SANDBOX_MODE', 'True').lower() == 'true'
    TRADINGVIEW_ONLY = os.getenv('TRADINGVIEW_ONLY', 'True').lower() == 'true'
    
    # Account Settings
    ACCOUNT_BALANCE = float(os.getenv('ACCOUNT_BALANCE', 1000.0))  # USD
    
    # Risk Management Settings 🛡️
    RISK_PERCENT = float(os.getenv('RISK_PERCENT', 1.0))  # Risk 1% per trade
    STOP_LOSS_PERCENT = float(os.getenv('STOP_LOSS_PERCENT', 2.0))  # 2% stop loss
    TAKE_PROFIT_PERCENT = float(os.getenv('TAKE_PROFIT_PERCENT', 4.0))  # 4% take profit
    
    # Position Limits
    MAX_POSITIONS = int(os.getenv('MAX_POSITIONS', 3))  # Max 3 open positions
    MAX_POSITION_PERCENT = float(os.getenv('MAX_POSITION_PERCENT', 10.0))  # Max 10% per position
    MIN_POSITION_SIZE = float(os.getenv('MIN_POSITION_SIZE', 0.001))  # Minimum trade size
    
    # Daily Limits
    MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', 50.0))  # Max $50 loss per day
    MAX_DAILY_TRADES = int(os.getenv('MAX_DAILY_TRADES', 10))  # Max 10 trades per day
    MAX_CONSECUTIVE_LOSSES = int(os.getenv('MAX_CONSECUTIVE_LOSSES', 3))  # Stop after 3 losses
    
    # Cooldown Settings
    TRADE_COOLDOWN_MINUTES = int(os.getenv('TRADE_COOLDOWN_MINUTES', 5))  # 5 min between trades
    
    # Supported Trading Pairs (start with one!)
    ALLOWED_SYMBOLS = [
        'BTCUSDT'  # Start with Bitcoin only
        # Add more later: 'ETHUSDT', 'ADAUSDT', 'DOTUSDT'
    ]
    
    # TradingView Webhook Settings
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your-secret-key')
    
    @classmethod
    def validate_config(cls):
        """Validate critical configuration"""
        errors = []
        
        if not cls.API_KEY:
            errors.append("API_KEY is required")
        
        if not cls.API_SECRET:
            errors.append("API_SECRET is required")
        
        if cls.RISK_PERCENT <= 0 or cls.RISK_PERCENT > 5:
            errors.append("RISK_PERCENT must be between 0.1 and 5.0")
        
        if cls.STOP_LOSS_PERCENT <= 0:
            errors.append("STOP_LOSS_PERCENT must be positive")
        
        if cls.ACCOUNT_BALANCE <= 0:
            errors.append("ACCOUNT_BALANCE must be positive")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True