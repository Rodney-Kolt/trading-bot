"""
Profitable Trading App - Enhanced Flask Server
Handles the profitable trading system with automation phases
"""

from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime
from profitable_bot import ProfitableTradingBot
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('profitable_trading.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# Initialize profitable trading bot
try:
    trading_bot = ProfitableTradingBot()
    logging.info("🚀 Profitable Trading Bot server started successfully")
except Exception as e:
    logging.error(f"Failed to initialize profitable trading bot: {str(e)}")
    trading_bot = None

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Enhanced webhook for profitable trading system
    Handles signals, trade executions, closures, and emergency stops
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        # Log incoming data
        action = data.get('action', 'UNKNOWN')
        logging.info(f"📡 Received: {action} | Data: {data}")
        
        # Check if bot is initialized
        if trading_bot is None:
            return jsonify({"error": "Trading bot not initialized"}), 500
        
        # Process the signal/event
        result = trading_bot.process_signal(data)
        
        return jsonify({"status": "success", "result": result}), 200
        
    except Exception as e:
        logging.error(f"Webhook error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Get comprehensive bot status"""
    try:
        if trading_bot is None:
            return jsonify({"error": "Trading bot not initialized"}), 500
        
        status_info = trading_bot.get_status()
        return jsonify(status_info), 200
    except Exception as e:
        logging.error(f"Status error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Enhanced health check"""
    try:
        health_info = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "bot_initialized": trading_bot is not None,
            "webhook_ready": True,
            "system_type": "profitable_trading_system"
        }
        
        if trading_bot:
            health_info.update({
                "automation_phase": trading_bot.automation_phase,
                "emergency_stop": trading_bot.emergency_stop,
                "daily_trades": trading_bot.daily_stats['trades'],
                "daily_pnl": trading_bot.daily_stats['pnl_percent']
            })
        
        return jsonify(health_info), 200
    except Exception as e:
        logging.error(f"Health check error: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/automation', methods=['POST'])
def set_automation():
    """Set automation phase"""
    try:
        if trading_bot is None:
            return jsonify({"error": "Trading bot not initialized"}), 500
        
        data = request.get_json()
        phase = data.get('phase', '').upper()
        
        result = trading_bot.set_automation_phase(phase)
        return jsonify(result), 200
        
    except Exception as e:
        logging.error(f"Automation setting error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/automation', methods=['GET'])
def get_automation():
    """Get current automation phase"""
    try:
        if trading_bot is None:
            return jsonify({"error": "Trading bot not initialized"}), 500
        
        return jsonify({
            "automation_phase": trading_bot.automation_phase,
            "available_phases": ["SIGNAL_ONLY", "SEMI_AUTO", "FULL_AUTO"],
            "emergency_stop": trading_bot.emergency_stop
        }), 200
        
    except Exception as e:
        logging.error(f"Automation get error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/emergency-stop', methods=['POST'])
def emergency_stop():
    """Manual emergency stop"""
    try:
        if trading_bot is None:
            return jsonify({"error": "Trading bot not initialized"}), 500
        
        trading_bot.emergency_stop = True
        logging.critical("🚨 MANUAL EMERGENCY STOP ACTIVATED")
        
        return jsonify({
            "status": "success",
            "message": "Emergency stop activated",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logging.error(f"Emergency stop error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/reset-emergency', methods=['POST'])
def reset_emergency():
    """Reset emergency stop"""
    try:
        if trading_bot is None:
            return jsonify({"error": "Trading bot not initialized"}), 500
        
        result = trading_bot.reset_emergency_stop()
        return jsonify(result), 200
        
    except Exception as e:
        logging.error(f"Reset emergency error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/profit', methods=['GET'])
def profit_info():
    """Get profit and withdrawal information"""
    try:
        if trading_bot is None:
            return jsonify({"error": "Trading bot not initialized"}), 500
        
        status = trading_bot.get_status()
        
        return jsonify({
            "profit_tracker": status['profit_tracker'],
            "withdrawal_recommendation": status['withdrawal_recommendation'],
            "daily_stats": status['daily_stats']
        }), 200
        
    except Exception as e:
        logging.error(f"Profit info error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/trades', methods=['GET'])
def get_trades():
    """Get trade history"""
    try:
        if trading_bot is None:
            return jsonify({"error": "Trading bot not initialized"}), 500
        
        limit = request.args.get('limit', 50, type=int)
        trades = trading_bot.trade_history[-limit:] if limit > 0 else trading_bot.trade_history
        
        return jsonify({
            "trades": trades,
            "total_count": len(trading_bot.trade_history),
            "returned_count": len(trades)
        }), 200
        
    except Exception as e:
        logging.error(f"Get trades error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.info("🚀 Starting Profitable Trading System...")
    logging.info(f"🎯 System Focus: Small wins, strict risk management")
    logging.info(f"🛡️ Max Risk: 0.5-1% per trade, 2% daily max loss")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)