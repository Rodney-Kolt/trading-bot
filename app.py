"""
Trading Bot - Webhook Receiver & Main Application
Handles TradingView alerts and coordinates trade execution
"""

from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime
from bot import TradingBot
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
trading_bot = TradingBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Receives TradingView alerts via webhook
    Expected payload: {"action": "BUY/SELL", "symbol": "BTCUSDT", "price": "50000"}
    """
    try:
        # Get alert data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        # Log incoming signal
        logging.info(f"Received signal: {data}")
        
        # Validate required fields
        required_fields = ['action', 'symbol', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        # Process the signal
        result = trading_bot.process_signal(data)
        
        return jsonify({"status": "success", "result": result}), 200
        
    except Exception as e:
        logging.error(f"Webhook error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Get bot status and recent trades"""
    try:
        status_info = trading_bot.get_status()
        return jsonify(status_info), 200
    except Exception as e:
        logging.error(f"Status error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "bot_running": trading_bot.is_running()
    }), 200

if __name__ == '__main__':
    logging.info("Starting Trading Bot...")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)