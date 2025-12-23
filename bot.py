"""
Trading Bot - Core Logic & Trade Execution Engine
Handles signal validation, risk management, and order execution
"""

import ccxt
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from risk import RiskManager
from config import Config

class TradingBot:
    def __init__(self):
        self.exchange = None
        self.exchange_connected = False
        self.risk_manager = RiskManager()
        self.positions = {}  # Track open positions
        self.trade_history = []
        self.last_trade_time = {}  # Cooldown tracking
        self.running = True
        
        # Try to connect to exchange, but don't fail if it's blocked
        try:
            self.exchange = self._setup_exchange()
            self.exchange_connected = True
            logging.info("Trading Bot initialized with exchange connection")
        except Exception as e:
            logging.warning(f"Exchange connection failed (will retry on first trade): {str(e)}")
            logging.info("Trading Bot initialized in webhook-only mode")
    
    def _setup_exchange(self):
        """Initialize exchange connection"""
        try:
            if Config.EXCHANGE == 'binance':
                exchange = ccxt.binance({
                    'apiKey': Config.API_KEY,
                    'secret': Config.API_SECRET,
                    'sandbox': Config.SANDBOX_MODE,
                    'enableRateLimit': True,
                })
            else:
                raise ValueError(f"Unsupported exchange: {Config.EXCHANGE}")
            
            # Test connection - but don't fail startup if blocked
            try:
                exchange.load_markets()
                logging.info(f"Connected to {Config.EXCHANGE}")
            except Exception as e:
                if "restricted location" in str(e) or "451" in str(e):
                    logging.warning(f"Exchange blocked by location - will work in webhook mode only")
                    # Don't load markets, but keep exchange object for later
                else:
                    raise e
            
            return exchange
            
        except Exception as e:
            logging.error(f"Exchange setup failed: {str(e)}")
            raise
    
    def process_signal(self, signal_data: Dict) -> Dict:
        """
        Main signal processing pipeline
        1. Validate signal
        2. Check risk rules
        3. Execute trade if approved
        """
        try:
            action = signal_data['action'].upper()
            symbol = signal_data['symbol']
            price = float(signal_data['price'])
            
            logging.info(f"Processing {action} signal for {symbol} at {price}")
            
            # Ensure exchange is connected
            if not self.exchange_connected:
                try:
                    self.exchange = self._setup_exchange()
                    self.exchange_connected = True
                except Exception as e:
                    return {"status": "error", "reason": f"Exchange connection failed: {str(e)}"}
            
            # Step 1: Signal validation
            if not self._validate_signal(signal_data):
                return {"status": "rejected", "reason": "Signal validation failed"}
            
            # Step 2: Risk management check
            risk_check = self.risk_manager.check_trade_allowed(
                symbol, action, price, self.positions
            )
            
            if not risk_check['allowed']:
                return {"status": "rejected", "reason": risk_check['reason']}
            
            # Step 3: Execute trade
            if action == 'BUY':
                result = self._execute_buy(symbol, price, risk_check['position_size'])
            elif action == 'SELL':
                result = self._execute_sell(symbol, price)
            else:
                return {"status": "rejected", "reason": f"Invalid action: {action}"}
            
            # Log trade
            self._log_trade(signal_data, result)
            
            return result
            
        except Exception as e:
            logging.error(f"Signal processing error: {str(e)}")
            return {"status": "error", "reason": str(e)}
    
    def _validate_signal(self, signal_data: Dict) -> bool:
        """
        Signal validation rules:
        - Check cooldown period
        - Verify allowed symbols
        - Validate strategy source
        - Check market conditions
        """
        symbol = signal_data['symbol']
        
        # Check if symbol is allowed
        if symbol not in Config.ALLOWED_SYMBOLS:
            logging.warning(f"Symbol not in allowed list: {symbol}")
            return False
        
        # Check cooldown (prevent spam trades)
        if symbol in self.last_trade_time:
            time_since_last = datetime.now() - self.last_trade_time[symbol]
            if time_since_last < timedelta(minutes=Config.TRADE_COOLDOWN_MINUTES):
                logging.warning(f"Trade cooldown active for {symbol}")
                return False
        
        # Only validate symbol exists if exchange is connected
        if self.exchange_connected and self.exchange:
            try:
                if symbol not in self.exchange.markets:
                    logging.error(f"Invalid symbol on exchange: {symbol}")
                    return False
            except Exception as e:
                logging.warning(f"Could not validate symbol on exchange: {str(e)}")
        
        # Check if strategy is recognized (optional validation)
        strategy = signal_data.get('strategy', 'unknown')
        if strategy not in ['EMA_RSI', 'unknown']:
            logging.warning(f"Unknown strategy: {strategy}")
        
        # Validate timeframe (prefer higher timeframes)
        timeframe = signal_data.get('timeframe', '15m')
        if timeframe not in ['15m', '1h', '4h', '1d']:
            logging.warning(f"Low timeframe detected: {timeframe}")
        
        return True
    
    def _execute_buy(self, symbol: str, price: float, position_size: float) -> Dict:
        """Execute BUY order"""
        try:
            # Check if already in position
            if symbol in self.positions:
                logging.warning(f"Already in position for {symbol}")
                return {"status": "rejected", "reason": "Already in position"}
            
            # Place market buy order
            order = self.exchange.create_market_buy_order(symbol, position_size)
            
            # Store position
            self.positions[symbol] = {
                'side': 'long',
                'size': position_size,
                'entry_price': order['average'] or price,
                'timestamp': datetime.now(),
                'order_id': order['id']
            }
            
            # Set stop loss and take profit
            self._set_stop_loss_take_profit(symbol, order['average'] or price)
            
            # Update cooldown
            self.last_trade_time[symbol] = datetime.now()
            
            logging.info(f"BUY executed: {symbol} - Size: {position_size} - Price: {order['average']}")
            
            return {
                "status": "executed",
                "action": "BUY",
                "symbol": symbol,
                "size": position_size,
                "price": order['average'],
                "order_id": order['id']
            }
            
        except Exception as e:
            logging.error(f"Buy execution failed: {str(e)}")
            return {"status": "error", "reason": str(e)}
    
    def _execute_sell(self, symbol: str, price: float) -> Dict:
        """Execute SELL order"""
        try:
            # Check if in position
            if symbol not in self.positions:
                logging.warning(f"No position to sell for {symbol}")
                return {"status": "rejected", "reason": "No position to sell"}
            
            position = self.positions[symbol]
            
            # Place market sell order
            order = self.exchange.create_market_sell_order(symbol, position['size'])
            
            # Calculate P&L
            entry_price = position['entry_price']
            exit_price = order['average'] or price
            pnl = (exit_price - entry_price) * position['size']
            pnl_percent = ((exit_price - entry_price) / entry_price) * 100
            
            # Remove position
            del self.positions[symbol]
            
            # Update cooldown
            self.last_trade_time[symbol] = datetime.now()
            
            logging.info(f"SELL executed: {symbol} - P&L: {pnl:.2f} ({pnl_percent:.2f}%)")
            
            return {
                "status": "executed",
                "action": "SELL",
                "symbol": symbol,
                "size": position['size'],
                "price": order['average'],
                "pnl": pnl,
                "pnl_percent": pnl_percent,
                "order_id": order['id']
            }
            
        except Exception as e:
            logging.error(f"Sell execution failed: {str(e)}")
            return {"status": "error", "reason": str(e)}
    
    def _set_stop_loss_take_profit(self, symbol: str, entry_price: float):
        """Set stop loss and take profit orders"""
        try:
            position = self.positions[symbol]
            
            # Calculate stop loss and take profit prices
            stop_loss_price = entry_price * (1 - Config.STOP_LOSS_PERCENT / 100)
            take_profit_price = entry_price * (1 + Config.TAKE_PROFIT_PERCENT / 100)
            
            # Note: This is simplified - in production you'd place actual stop orders
            position['stop_loss'] = stop_loss_price
            position['take_profit'] = take_profit_price
            
            logging.info(f"Stop Loss: {stop_loss_price:.2f}, Take Profit: {take_profit_price:.2f}")
            
        except Exception as e:
            logging.error(f"Failed to set stop loss/take profit: {str(e)}")
    
    def _log_trade(self, signal_data: Dict, result: Dict):
        """Log trade to history"""
        trade_log = {
            'timestamp': datetime.now().isoformat(),
            'signal': signal_data,
            'result': result
        }
        self.trade_history.append(trade_log)
        
        # Keep only last 1000 trades
        if len(self.trade_history) > 1000:
            self.trade_history = self.trade_history[-1000:]
    
    def get_status(self) -> Dict:
        """Get current bot status"""
        try:
            status = {
                'running': self.running,
                'exchange_connected': self.exchange_connected,
                'positions': self.positions,
                'recent_trades': self.trade_history[-10:],  # Last 10 trades
                'total_trades': len(self.trade_history)
            }
            
            # Try to get balance if exchange is connected
            if self.exchange_connected and self.exchange:
                try:
                    balance = self.exchange.fetch_balance()
                    status['balance'] = balance['total']
                except Exception as e:
                    status['balance_error'] = str(e)
            else:
                status['balance'] = 'Exchange not connected'
            
            return status
            
        except Exception as e:
            logging.error(f"Status check failed: {str(e)}")
            return {'error': str(e)}
    
    def is_running(self) -> bool:
        """Check if bot is running"""
        return self.running