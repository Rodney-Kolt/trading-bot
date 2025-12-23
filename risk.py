"""
Risk Management System - The Shield 🛡️
Protects your capital with position sizing, stop loss, and risk limits
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from config import Config

class RiskManager:
    def __init__(self):
        self.daily_loss = 0.0
        self.daily_trades = 0
        self.last_reset_date = datetime.now().date()
        self.consecutive_losses = 0
        
        logging.info("Risk Manager initialized")
    
    def check_trade_allowed(self, symbol: str, action: str, price: float, positions: Dict) -> Dict:
        """
        Master risk check - ALL trades must pass this
        Returns: {"allowed": bool, "reason": str, "position_size": float}
        """
        
        # Reset daily counters if new day
        self._reset_daily_counters_if_needed()
        
        # Risk Rule 1: Daily loss limit
        if self.daily_loss >= Config.MAX_DAILY_LOSS:
            return {
                "allowed": False,
                "reason": f"Daily loss limit reached: ${self.daily_loss:.2f}",
                "position_size": 0
            }
        
        # Risk Rule 2: Maximum daily trades
        if self.daily_trades >= Config.MAX_DAILY_TRADES:
            return {
                "allowed": False,
                "reason": f"Daily trade limit reached: {self.daily_trades}",
                "position_size": 0
            }
        
        # Risk Rule 3: Consecutive loss cooldown
        if self.consecutive_losses >= Config.MAX_CONSECUTIVE_LOSSES:
            return {
                "allowed": False,
                "reason": f"Too many consecutive losses: {self.consecutive_losses}",
                "position_size": 0
            }
        
        # Risk Rule 4: Maximum positions
        if action == 'BUY' and len(positions) >= Config.MAX_POSITIONS:
            return {
                "allowed": False,
                "reason": f"Maximum positions reached: {len(positions)}",
                "position_size": 0
            }
        
        # Risk Rule 5: No double positions
        if action == 'BUY' and symbol in positions:
            return {
                "allowed": False,
                "reason": f"Already in position for {symbol}",
                "position_size": 0
            }
        
        # Risk Rule 6: Must have position to sell
        if action == 'SELL' and symbol not in positions:
            return {
                "allowed": False,
                "reason": f"No position to sell for {symbol}",
                "position_size": 0
            }
        
        # Calculate position size
        position_size = self._calculate_position_size(price)
        
        # Risk Rule 7: Minimum position size
        if position_size < Config.MIN_POSITION_SIZE:
            return {
                "allowed": False,
                "reason": f"Position size too small: {position_size}",
                "position_size": 0
            }
        
        # All checks passed ✅
        return {
            "allowed": True,
            "reason": "All risk checks passed",
            "position_size": position_size
        }
    
    def _calculate_position_size(self, price: float) -> float:
        """
        Calculate position size based on risk percentage
        Risk 1-2% of account per trade
        """
        try:
            # This is simplified - in production you'd get actual account balance
            account_balance = Config.ACCOUNT_BALANCE
            
            # Risk amount (1-2% of account)
            risk_amount = account_balance * (Config.RISK_PERCENT / 100)
            
            # Position size = Risk Amount / (Entry Price * Stop Loss %)
            stop_loss_amount = price * (Config.STOP_LOSS_PERCENT / 100)
            position_size = risk_amount / stop_loss_amount
            
            # Apply maximum position size limit
            max_position_value = account_balance * (Config.MAX_POSITION_PERCENT / 100)
            max_position_size = max_position_value / price
            
            position_size = min(position_size, max_position_size)
            
            logging.info(f"Calculated position size: {position_size:.6f} (Risk: ${risk_amount:.2f})")
            
            return round(position_size, 6)
            
        except Exception as e:
            logging.error(f"Position size calculation failed: {str(e)}")
            return 0.0
    
    def record_trade_result(self, pnl: float):
        """
        Record trade result for risk tracking
        Updates daily loss and consecutive loss counters
        """
        self.daily_trades += 1
        
        if pnl < 0:
            # Loss
            self.daily_loss += abs(pnl)
            self.consecutive_losses += 1
            logging.warning(f"Trade loss recorded: ${pnl:.2f} (Consecutive: {self.consecutive_losses})")
        else:
            # Profit - reset consecutive losses
            self.consecutive_losses = 0
            logging.info(f"Trade profit recorded: ${pnl:.2f}")
        
        # Check if we need emergency stop
        if self.daily_loss >= Config.MAX_DAILY_LOSS:
            logging.critical("🚨 DAILY LOSS LIMIT REACHED - TRADING STOPPED 🚨")
        
        if self.consecutive_losses >= Config.MAX_CONSECUTIVE_LOSSES:
            logging.critical("🚨 TOO MANY CONSECUTIVE LOSSES - TRADING STOPPED 🚨")
    
    def _reset_daily_counters_if_needed(self):
        """Reset daily counters at start of new day"""
        current_date = datetime.now().date()
        
        if current_date > self.last_reset_date:
            logging.info("New day - resetting daily risk counters")
            self.daily_loss = 0.0
            self.daily_trades = 0
            self.last_reset_date = current_date
    
    def get_risk_status(self) -> Dict:
        """Get current risk status"""
        return {
            'daily_loss': self.daily_loss,
            'daily_trades': self.daily_trades,
            'consecutive_losses': self.consecutive_losses,
            'max_daily_loss': Config.MAX_DAILY_LOSS,
            'max_daily_trades': Config.MAX_DAILY_TRADES,
            'max_consecutive_losses': Config.MAX_CONSECUTIVE_LOSSES,
            'risk_percent': Config.RISK_PERCENT,
            'trading_allowed': (
                self.daily_loss < Config.MAX_DAILY_LOSS and
                self.daily_trades < Config.MAX_DAILY_TRADES and
                self.consecutive_losses < Config.MAX_CONSECUTIVE_LOSSES
            )
        }
    
    def emergency_stop(self):
        """Emergency stop all trading"""
        logging.critical("🚨 EMERGENCY STOP ACTIVATED 🚨")
        self.daily_loss = Config.MAX_DAILY_LOSS  # This will block all trades
    
    def reset_consecutive_losses(self):
        """Manual reset of consecutive losses (admin function)"""
        logging.info("Consecutive losses manually reset")
        self.consecutive_losses = 0