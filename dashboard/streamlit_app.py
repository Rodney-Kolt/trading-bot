"""
Trading Bot Dashboard - Streamlit Interface
Real-time monitoring of signals, trades, and performance
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json

# Page config
st.set_page_config(
    page_title="Trading Bot Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
BOT_URL = st.secrets.get("BOT_URL", "https://your-app.railway.app")

def get_bot_status():
    """Get bot status from Railway-hosted bot"""
    try:
        response = requests.get(f"{BOT_URL}/status", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_bot_health():
    """Get bot health check"""
    try:
        response = requests.get(f"{BOT_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

def send_test_signal(action, symbol, price):
    """Send test signal to bot"""
    try:
        data = {
            "action": action,
            "symbol": symbol,
            "price": str(price),
            "strategy": "DASHBOARD_TEST",
            "timeframe": "15m"
        }
        response = requests.post(f"{BOT_URL}/webhook", json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Main Dashboard
def main():
    st.title("🤖 Trading Bot Dashboard")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Bot URL configuration
        bot_url = st.text_input("Bot URL", value=BOT_URL, help="Your Railway app URL")
        if bot_url != BOT_URL:
            st.session_state.bot_url = bot_url
        
        st.markdown("---")
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto Refresh", value=True)
        refresh_interval = st.slider("Refresh Interval (seconds)", 5, 60, 10)
        
        if st.button("🔄 Refresh Now"):
            st.rerun()
        
        st.markdown("---")
        
        # Test signals
        st.subheader("🧪 Test Signals")
        test_symbol = st.selectbox("Symbol", ["BTCUSDT", "ETHUSDT", "EURUSD"])
        test_price = st.number_input("Price", value=50000.0, step=100.0)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 Send BUY"):
                result = send_test_signal("BUY", test_symbol, test_price)
                st.json(result)
        
        with col2:
            if st.button("📉 Send SELL"):
                result = send_test_signal("SELL", test_symbol, test_price)
                st.json(result)
    
    # Main content
    # Health Status
    health = get_bot_health()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if health.get("status") == "healthy":
            st.success("🟢 Bot Online")
        else:
            st.error("🔴 Bot Offline")
    
    with col2:
        webhook_ready = health.get("webhook_ready", False)
        if webhook_ready:
            st.success("📡 Webhook Ready")
        else:
            st.warning("📡 Webhook Not Ready")
    
    with col3:
        exchange_connected = health.get("exchange_connected", False)
        if exchange_connected:
            st.success("🏦 Exchange Connected")
        else:
            st.info("🏦 Simulation Mode")
    
    with col4:
        bot_initialized = health.get("bot_initialized", False)
        if bot_initialized:
            st.success("⚙️ Bot Initialized")
        else:
            st.error("⚙️ Bot Not Initialized")
    
    st.markdown("---")
    
    # Get bot status
    status = get_bot_status()
    
    if "error" in status:
        st.error(f"❌ Cannot connect to bot: {status['error']}")
        st.info("Make sure your bot is running on Railway and the URL is correct.")
        return
    
    # Performance Overview
    st.header("📊 Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        mode = status.get('mode', 'Unknown')
        st.metric("Mode", mode)
    
    with col2:
        total_trades = status.get('total_trades', 0)
        st.metric("Total Trades", total_trades)
    
    with col3:
        if 'paper_balance' in status:
            current_balance = status['paper_balance']
            starting_balance = status.get('starting_balance', 1000)
            st.metric("Balance", f"${current_balance:.2f}", f"${current_balance - starting_balance:.2f}")
        else:
            balance = status.get('balance', 'N/A')
            st.metric("Balance", balance)
    
    with col4:
        if 'total_pnl_percent' in status:
            pnl_percent = status['total_pnl_percent']
            st.metric("Total Return", f"{pnl_percent:.2f}%")
        else:
            st.metric("Total Return", "N/A")
    
    # Current Positions
    st.header("📍 Current Positions")
    
    positions = status.get('positions', {})
    if positions:
        positions_data = []
        for symbol, pos in positions.items():
            positions_data.append({
                'Symbol': symbol,
                'Side': pos.get('side', 'N/A').upper(),
                'Size': pos.get('size', 0),
                'Entry Price': f"${pos.get('entry_price', 0):.2f}",
                'Timestamp': pos.get('timestamp', 'N/A'),
                'Type': 'Simulated' if pos.get('simulated') else 'Real'
            })
        
        df_positions = pd.DataFrame(positions_data)
        st.dataframe(df_positions, use_container_width=True)
    else:
        st.info("No open positions")
    
    # Recent Trades
    st.header("📈 Recent Trades")
    
    recent_trades = status.get('recent_trades', [])
    if recent_trades:
        trades_data = []
        for trade in recent_trades[-10:]:  # Last 10 trades
            signal = trade.get('signal', {})
            result = trade.get('result', {})
            
            trades_data.append({
                'Timestamp': trade.get('timestamp', 'N/A'),
                'Action': signal.get('action', 'N/A'),
                'Symbol': signal.get('symbol', 'N/A'),
                'Price': f"${float(signal.get('price', 0)):.2f}",
                'Status': result.get('status', 'N/A'),
                'P&L': f"${result.get('pnl', 0):.2f}" if 'pnl' in result else 'N/A',
                'Mode': result.get('mode', 'N/A')
            })
        
        df_trades = pd.DataFrame(trades_data)
        st.dataframe(df_trades, use_container_width=True)
        
        # P&L Chart
        if any('pnl' in trade.get('result', {}) for trade in recent_trades):
            st.subheader("📊 P&L Chart")
            
            pnl_data = []
            cumulative_pnl = 0
            
            for trade in recent_trades:
                result = trade.get('result', {})
                if 'pnl' in result:
                    cumulative_pnl += result['pnl']
                    pnl_data.append({
                        'Trade': len(pnl_data) + 1,
                        'P&L': result['pnl'],
                        'Cumulative P&L': cumulative_pnl,
                        'Timestamp': trade.get('timestamp', '')
                    })
            
            if pnl_data:
                df_pnl = pd.DataFrame(pnl_data)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_pnl['Trade'],
                    y=df_pnl['Cumulative P&L'],
                    mode='lines+markers',
                    name='Cumulative P&L',
                    line=dict(color='green' if df_pnl['Cumulative P&L'].iloc[-1] > 0 else 'red')
                ))
                
                fig.update_layout(
                    title="Cumulative P&L Over Time",
                    xaxis_title="Trade Number",
                    yaxis_title="P&L ($)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trades yet")
    
    # Raw Status (for debugging)
    with st.expander("🔍 Raw Bot Status (Debug)"):
        st.json(status)
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()