"""
Profitable Trading Bot - Risk Guardian & Automation Controller
Enhanced version focused on small wins and strict risk management
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from risk import RiskManager
from config import Config

class ProfitableTradingBot:
    def __init__(self):
        self.risk_manager = RiskManager()
        self.automation_phase = "SIGNAL_ONLY"  # SIGNAL_ONLY, SEMI_AUTO, FULL_AUTO
        self.daily_stats = {
            'trades': 0,
            'wins': 0,
            'losses': 0,
            'pnl_percent': 0.0,
            'consecutive_losses': 0,
            'last_reset': datetime.now().date()
        }
        self.profit_tracker = {
            'starting_balance': Config.ACCOUNT_BALANCE,
            'current_balance': Config.ACCOUNT_BALANCE,
            'total_profit': 0.0,
            'withdrawable_profit': 0.0,
            'last_withdrawal': 0.0
        }
        self.emergency_stop = False
        self.trade_history = []
        
        # Multi-currency support
        self.supported_currencies = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'EURJPY', 'GBPJPY', 'EURGBP']
        self.currency_stats = {}
        for currency in self.supported_currencies:
            self.currency_stats[currency] = {
                'signals_today': 0,
                'trades_today': 0,
                'wins': 0,
                'losses': 0,
                'pnl': 0.0,
                'last_signal': None
            }
        
        logging.info("🚀 Multi-Currency Profitable Trading Bot initialized")
        logging.info(f"📊 Automation Phase: {self.automation_phase}")
        logging.info(f"💰 Starting Balance: ${Config.ACCOUNT_BALANCE}")
        logging.info(f"🌍 Supported Currencies: {', '.join(self.supported_currencies)}")
    
    def process_signal(self, signal_data: Dict) -> Dict:
        """
        Enhanced signal processing with automation phases
        """
        try:
            action = signal_data.get('action', '').upper()
            
            # Handle different message types
            if action == "EMERGENCY_STOP":
                return self._handle_emergency_stop(signal_data)
            elif action == "TRADE_EXECUTED":
                return self._handle_trade_execution(signal_data)
            elif action == "TRADE_CLOSED":
                return self._handle_trade_closure(signal_data)
            elif action in ["BUY", "SELL"]:
                return self._handle_trading_signal(signal_data)
            else:
                return {"status": "unknown_action", "action": action}
                
        except Exception as e:
            logging.error(f"Signal processing error: {str(e)}")
            return {"status": "error", "reason": str(e)}
    
    def _handle_trading_signal(self, signal_data: Dict) -> Dict:
        """Handle BUY/SELL signals based on automation phase with multi-currency support"""
        
        # Reset daily stats if new day
        self._check_new_day()
        
        # Check if emergency stop is active
        if self.emergency_stop:
            return {"status": "rejected", "reason": "Emergency stop active"}
        
        action = signal_data['action']
        symbol = signal_data.get('symbol', 'UNKNOWN')
        price = float(signal_data.get('price', 0))
        strategy = signal_data.get('strategy', 'UNKNOWN')
        timeframe = signal_data.get('timeframe', '15m')
        
        logging.info(f"📊 {action} Signal: {symbol} @ {price} | Strategy: {strategy} | TF: {timeframe}")
        
        # Update currency stats
        if symbol in self.currency_stats:
            self.currency_stats[symbol]['signals_today'] += 1
            self.currency_stats[symbol]['last_signal'] = datetime.now().isoformat()
        
        # Log signal regardless of automation phase
        signal_log = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'symbol': symbol,
            'price': price,
            'strategy': strategy,
            'timeframe': timeframe,
            'automation_phase': self.automation_phase,
            'status': 'signal_received'
        }
        self.trade_history.append(signal_log)
        
        # Process based on automation phase
        if self.automation_phase == "SIGNAL_ONLY":
            return {
                "status": "logged",
                "message": f"{symbol} {action} signal logged - Auto trading disabled",
                "automation_phase": self.automation_phase,
                "symbol": symbol,
                "action": action,
                "price": price
            }
        
        elif self.automation_phase == "SEMI_AUTO":
            return self._process_semi_auto_signal(signal_log)
        
        elif self.automation_phase == "FULL_AUTO":
            return self._process_full_auto_signal(signal_log)
        
        else:
            return {"status": "error", "reason": "Unknown automation phase"}
            # In semi-auto, we validate but don't execute
            validation = self._validate_trade_conditions(signal_data)
            return {
                "status": "validated",
                "validation": validation,
                "automation_phase": self.automation_phase,
                "message": "Trade validated - Manual execution required"
            }
        
        elif self.automation_phase == "FULL_AUTO":
            # In full auto, EA handles execution, we just validate and log
            validation = self._validate_trade_conditions(signal_data)
            if not validation['allowed']:
                logging.warning(f"Trade validation failed: {validation['reason']}")
            
            return {
                "status": "processed",
                "validation": validation,
                "automation_phase": self.automation_phase,
                "message": "Signal processed - EA handles execution"
            }
        
        return {"status": "unknown_phase", "automation_phase": self.automation_phase}
    
    def _handle_trade_execution(self, signal_data: Dict) -> Dict:
        """Handle trade execution confirmation from MT5 EA"""
        
        symbol = signal_data.get('symbol', 'UNKNOWN')
        side = signal_data.get('side', 'UNKNOWN')
        price = float(signal_data.get('price', 0))
        lot_size = float(signal_data.get('lot_size', 0))
        stop_loss = float(signal_data.get('stop_loss', 0))
        take_profit = float(signal_data.get('take_profit', 0))
        reason = signal_data.get('reason', 'NO_REASON')
        daily_trades = int(signal_data.get('daily_trades', 0))
        
        logging.info(f"✅ Trade Executed: {side} {symbol} @ {price} | Lot: {lot_size} | SL: {stop_loss} | TP: {take_profit}")
        
        # Update daily stats
        self.daily_stats['trades'] = daily_trades
        
        # Log trade execution
        trade_log = {
            'timestamp': datetime.now().isoformat(),
            'action': 'TRADE_EXECUTED',
            'symbol': symbol,
            'side': side,
            'price': price,
            'lot_size': lot_size,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'reason': reason,
            'daily_trades': daily_trades,
            'status': 'executed'
        }
        self.trade_history.append(trade_log)
        
        return {
            "status": "trade_logged",
            "message": f"{side} trade executed and logged",
            "daily_trades": daily_trades
        }
    
    def _handle_trade_closure(self, signal_data: Dict) -> Dict:
        """Handle trade closure and P&L update"""
        
        symbol = signal_data.get('symbol', 'UNKNOWN')
        profit_percent = float(signal_data.get('profit_percent', 0))
        is_win = signal_data.get('is_win', False)
        daily_pnl = float(signal_data.get('daily_pnl', 0))
        consecutive_losses = int(signal_data.get('consecutive_losses', 0))
        
        logging.info(f"📊 Trade Closed: {symbol} | P&L: {profit_percent:.3f}% | Win: {is_win} | Daily: {daily_pnl:.2f}%")
        
        # Update daily stats
        self.daily_stats['pnl_percent'] = daily_pnl
        self.daily_stats['consecutive_losses'] = consecutive_losses
        
        if is_win:
            self.daily_stats['wins'] += 1
        else:
            self.daily_stats['losses'] += 1
        
        # Update profit tracker
        self._update_profit_tracker(profit_percent)
        
        # Log trade closure
        trade_log = {
            'timestamp': datetime.now().isoformat(),
            'action': 'TRADE_CLOSED',
            'symbol': symbol,
            'profit_percent': profit_percent,
            'is_win': is_win,
            'daily_pnl': daily_pnl,
            'consecutive_losses': consecutive_losses,
            'status': 'closed'
        }
        self.trade_history.append(trade_log)
        
        # Check for withdrawal recommendation
        withdrawal_rec = self._check_withdrawal_recommendation()
        
        return {
            "status": "trade_closed",
            "profit_percent": profit_percent,
            "is_win": is_win,
            "daily_pnl": daily_pnl,
            "withdrawal_recommendation": withdrawal_rec
        }
    
    def _handle_emergency_stop(self, signal_data: Dict) -> Dict:
        """Handle emergency stop from MT5 EA"""
        
        alert_type = signal_data.get('alert_type', 'UNKNOWN')
        daily_pnl = float(signal_data.get('daily_pnl', 0))
        daily_trades = int(signal_data.get('daily_trades', 0))
        consecutive_losses = int(signal_data.get('consecutive_losses', 0))
        
        logging.critical(f"🚨 EMERGENCY STOP: {alert_type} | P&L: {daily_pnl}% | Trades: {daily_trades} | Losses: {consecutive_losses}")
        
        self.emergency_stop = True
        self.daily_stats['pnl_percent'] = daily_pnl
        self.daily_stats['trades'] = daily_trades
        self.daily_stats['consecutive_losses'] = consecutive_losses
        
        # Log emergency stop
        emergency_log = {
            'timestamp': datetime.now().isoformat(),
            'action': 'EMERGENCY_STOP',
            'alert_type': alert_type,
            'daily_pnl': daily_pnl,
            'daily_trades': daily_trades,
            'consecutive_losses': consecutive_losses,
            'status': 'emergency_stop'
        }
        self.trade_history.append(emergency_log)
        
        return {
            "status": "emergency_stop_activated",
            "alert_type": alert_type,
            "message": "Trading stopped due to risk limits"
        }
    
    def _validate_trade_conditions(self, signal_data: Dict) -> Dict:
        """Validate if trade should be allowed"""
        
        # Basic validation
        if self.emergency_stop:
            return {"allowed": False, "reason": "Emergency stop active"}
        
        if self.daily_stats['trades'] >= 5:  # Max trades per day
            return {"allowed": False, "reason": "Daily trade limit reached"}
        
        if self.daily_stats['pnl_percent'] <= -2.0:  # Max daily loss
            return {"allowed": False, "reason": "Daily loss limit reached"}
        
        if self.daily_stats['consecutive_losses'] >= 2:  # Max consecutive losses
            return {"allowed": False, "reason": "Too many consecutive losses"}
        
        return {"allowed": True, "reason": "All conditions passed"}
    
    def _update_profit_tracker(self, profit_percent: float):
        """Update profit tracking"""
        
        profit_amount = (profit_percent / 100) * self.profit_tracker['starting_balance']
        self.profit_tracker['total_profit'] += profit_amount
        self.profit_tracker['current_balance'] += profit_amount
        
        # Calculate withdrawable profit (keep some buffer for trading)
        buffer_amount = self.profit_tracker['starting_balance'] * 0.1  # 10% buffer
        self.profit_tracker['withdrawable_profit'] = max(0, 
            self.profit_tracker['total_profit'] - buffer_amount)
    
    def _check_withdrawal_recommendation(self) -> Dict:
        """Check if withdrawal is recommended"""
        
        total_return = (self.profit_tracker['total_profit'] / self.profit_tracker['starting_balance']) * 100
        
        # Recommend withdrawal if:
        # 1. Weekly profit > 5%
        # 2. Total profit > $100
        # 3. Withdrawable amount > $50
        
        should_withdraw = (
            total_return >= 5.0 and 
            self.profit_tracker['total_profit'] >= 100 and
            self.profit_tracker['withdrawable_profit'] >= 50
        )
        
        return {
            "should_withdraw": should_withdraw,
            "withdrawable_amount": self.profit_tracker['withdrawable_profit'],
            "total_return_percent": total_return,
            "message": "Consider withdrawing profits" if should_withdraw else "Continue trading"
        }
    
    def _check_new_day(self):
        """Check if it's a new day and reset counters"""
        
        today = datetime.now().date()
        if today != self.daily_stats['last_reset']:
            logging.info(f"📅 New day - Resetting daily stats")
            logging.info(f"📊 Yesterday: {self.daily_stats}")
            
            self.daily_stats = {
                'trades': 0,
                'wins': 0,
                'losses': 0,
                'pnl_percent': 0.0,
                'consecutive_losses': 0,
                'last_reset': today
            }
            self.emergency_stop = False  # Reset emergency stop for new day
    
    def set_automation_phase(self, phase: str) -> Dict:
        """Set automation phase"""
        
        valid_phases = ["SIGNAL_ONLY", "SEMI_AUTO", "FULL_AUTO"]
        if phase not in valid_phases:
            return {"status": "error", "message": f"Invalid phase. Must be one of: {valid_phases}"}
        
        old_phase = self.automation_phase
        self.automation_phase = phase
        
        logging.info(f"🔄 Automation phase changed: {old_phase} → {phase}")
        
        return {
            "status": "success",
            "old_phase": old_phase,
            "new_phase": phase,
            "message": f"Automation phase set to {phase}"
        }
    
    def get_status(self) -> Dict:
        """Get comprehensive bot status"""
        
        self._check_new_day()
        
        # Calculate win rate
        total_closed = self.daily_stats['wins'] + self.daily_stats['losses']
        win_rate = (self.daily_stats['wins'] / total_closed * 100) if total_closed > 0 else 0
        
        return {
            'running': True,
            'automation_phase': self.automation_phase,
            'emergency_stop': self.emergency_stop,
            'daily_stats': {
                **self.daily_stats,
                'win_rate': win_rate,
                'total_closed_trades': total_closed
            },
            'profit_tracker': self.profit_tracker,
            'withdrawal_recommendation': self._check_withdrawal_recommendation(),
            'recent_trades': self.trade_history[-10:],
            'total_signals': len(self.trade_history)
        }
    
    def reset_emergency_stop(self) -> Dict:
        """Manual reset of emergency stop (admin function)"""
        
        self.emergency_stop = False
        logging.info("🔄 Emergency stop manually reset")
        
        return {
            "status": "success",
            "message": "Emergency stop reset - Trading can resume"
        }
    def _process_semi_auto_signal(self, signal_log: Dict) -> Dict:
        """Process signal in semi-automatic mode"""
        # In semi-auto, we validate but don't execute automatically
        validation = self.risk_manager.validate_trade(
            signal_log['symbol'], 
            signal_log['action'], 
            float(signal_log['price'])
        )
        
        if validation['valid']:
            return {
                "status": "validated",
                "message": f"{signal_log['symbol']} {signal_log['action']} signal validated - Manual approval required",
                "validation": validation,
                "signal": signal_log
            }
        else:
            return {
                "status": "rejected",
                "reason": validation['reason'],
                "signal": signal_log
            }
    
    def _process_full_auto_signal(self, signal_log: Dict) -> Dict:
        """Process signal in full automatic mode"""
        # Check daily limits
        if self.daily_stats['trades'] >= 5:
            return {"status": "rejected", "reason": "Daily trade limit reached"}
        
        if self.daily_stats['pnl_percent'] <= -2.0:
            return {"status": "rejected", "reason": "Daily loss limit reached"}
        
        # Validate trade
        validation = self.risk_manager.validate_trade(
            signal_log['symbol'], 
            signal_log['action'], 
            float(signal_log['price'])
        )
        
        if validation['valid']:
            # Execute trade automatically
            trade_result = self._execute_trade(signal_log)
            return trade_result
        else:
            return {
                "status": "rejected",
                "reason": validation['reason'],
                "signal": signal_log
            }
    
    def _execute_trade(self, signal_log: Dict) -> Dict:
        """Execute trade in simulation mode"""
        # Simulate trade execution
        self.daily_stats['trades'] += 1
        
        # Update currency stats
        symbol = signal_log['symbol']
        if symbol in self.currency_stats:
            self.currency_stats[symbol]['trades_today'] += 1
        
        # Simulate profit/loss (for demo purposes)
        import random
        win_rate = 0.65  # 65% win rate for small wins strategy
        
        if random.random() < win_rate:
            # Win
            profit_percent = random.uniform(0.4, 0.8)  # 0.4-0.8% profit
            self.daily_stats['wins'] += 1
            self.daily_stats['consecutive_losses'] = 0
            if symbol in self.currency_stats:
                self.currency_stats[symbol]['wins'] += 1
                self.currency_stats[symbol]['pnl'] += profit_percent
        else:
            # Loss
            profit_percent = -0.5  # Fixed 0.5% loss (tight stop)
            self.daily_stats['losses'] += 1
            self.daily_stats['consecutive_losses'] += 1
            if symbol in self.currency_stats:
                self.currency_stats[symbol]['losses'] += 1
                self.currency_stats[symbol]['pnl'] += profit_percent
        
        self.daily_stats['pnl_percent'] += profit_percent
        
        # Update profit tracker
        profit_amount = (profit_percent / 100) * self.profit_tracker['current_balance']
        self.profit_tracker['current_balance'] += profit_amount
        self.profit_tracker['total_profit'] += profit_amount
        
        if self.profit_tracker['total_profit'] > 0:
            self.profit_tracker['withdrawable_profit'] = self.profit_tracker['total_profit'] * 0.8
        
        return {
            "status": "executed",
            "message": f"{symbol} {signal_log['action']} trade executed",
            "profit_percent": profit_percent,
            "new_balance": self.profit_tracker['current_balance'],
            "signal": signal_log
        }
    
    def _check_new_day(self):
        """Reset daily stats if new day"""
        today = datetime.now().date()
        if self.daily_stats['last_reset'] != today:
            self.daily_stats = {
                'trades': 0,
                'wins': 0,
                'losses': 0,
                'pnl_percent': 0.0,
                'consecutive_losses': 0,
                'last_reset': today
            }
            # Reset currency daily stats
            for currency in self.currency_stats:
                self.currency_stats[currency]['signals_today'] = 0
                self.currency_stats[currency]['trades_today'] = 0
    
    def _handle_emergency_stop(self, signal_data: Dict) -> Dict:
        """Handle emergency stop signal"""
        self.emergency_stop = True
        logging.warning("🚨 EMERGENCY STOP ACTIVATED")
        return {"status": "emergency_stop_activated"}
    
    def _handle_trade_execution(self, signal_data: Dict) -> Dict:
        """Handle trade execution notification"""
        return {"status": "trade_execution_logged"}
    
    def _handle_trade_closure(self, signal_data: Dict) -> Dict:
        """Handle trade closure notification"""
        return {"status": "trade_closure_logged"}
    
    def get_status(self) -> Dict:
        """Get comprehensive bot status including multi-currency data"""
        return {
            "automation_phase": self.automation_phase,
            "emergency_stop": self.emergency_stop,
            "daily_stats": self.daily_stats,
            "profit_tracker": self.profit_tracker,
            "currency_stats": self.currency_stats,
            "supported_currencies": self.supported_currencies,
            "recent_signals": self.trade_history[-10:] if self.trade_history else []
        }
    
    def set_automation_phase(self, phase: str) -> bool:
        """Set automation phase"""
        valid_phases = ["SIGNAL_ONLY", "SEMI_AUTO", "FULL_AUTO"]
        if phase in valid_phases:
            self.automation_phase = phase
            logging.info(f"🔄 Automation phase changed to: {phase}")
            return True
        return False
    
    def toggle_emergency_stop(self) -> bool:
        """Toggle emergency stop"""
        self.emergency_stop = not self.emergency_stop
        status = "ACTIVATED" if self.emergency_stop else "DEACTIVATED"
        logging.warning(f"🚨 Emergency stop {status}")
        return self.emergency_stop