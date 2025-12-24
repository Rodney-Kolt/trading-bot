"""
Profitable Trading Dashboard - Enhanced Control Center
Real-time monitoring with automation controls and profit tracking
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
    page_title="Profitable Trading Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
BOT_URL = st.secrets.get("BOT_URL", "https://trading-bot-production-c863.up.railway.app")

def get_bot_status():
    """Get comprehensive bot status"""
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

def get_automation_status():
    """Get automation phase status"""
    try:
        response = requests.get(f"{BOT_URL}/automation", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def set_automation_phase(phase):
    """Set automation phase"""
    try:
        response = requests.post(f"{BOT_URL}/automation", 
                               json={"phase": phase}, 
                               timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def emergency_stop():
    """Trigger emergency stop"""
    try:
        response = requests.post(f"{BOT_URL}/emergency-stop", timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def reset_emergency():
    """Reset emergency stop"""
    try:
        response = requests.post(f"{BOT_URL}/reset-emergency", timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_profit_info():
    """Get profit and withdrawal information"""
    try:
        response = requests.get(f"{BOT_URL}/profit", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def send_test_signal(action, symbol, price):
    """Send test signal to bot"""
    try:
        data = {
            "action": action,
            "symbol": symbol,
            "price": str(price),
            "strategy": "DASHBOARD_TEST",
            "reason": "MANUAL_TEST",
            "timeframe": "15m"
        }
        response = requests.post(f"{BOT_URL}/webhook", json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Main Dashboard
def main():
    st.title("💰 Profitable Trading Dashboard")
    st.markdown("**Small-Wins Automated Trading System**")
    st.markdown("---")
    
    # Sidebar Controls
    with st.sidebar:
        st.header("🎛️ System Controls")
        
        # Bot URL configuration
        bot_url = st.text_input("Bot URL", value=BOT_URL, help="Your Railway app URL")
        
        st.markdown("---")
        
        # Automation Phase Control
        st.subheader("🤖 Automation Phase")
        
        automation_status = get_automation_status()
        if "error" not in automation_status:
            current_phase = automation_status.get("automation_phase", "UNKNOWN")
            emergency_active = automation_status.get("emergency_stop", False)
            
            # Phase selector
            phases = ["SIGNAL_ONLY", "SEMI_AUTO", "FULL_AUTO"]
            phase_descriptions = {
                "SIGNAL_ONLY": "📊 Signals only, no trading",
                "SEMI_AUTO": "⚠️ Validate trades, manual approval",
                "FULL_AUTO": "🚀 Fully automated trading"
            }
            
            st.write(f"**Current Phase:** {current_phase}")
            
            new_phase = st.selectbox(
                "Select Phase:",
                phases,
                index=phases.index(current_phase) if current_phase in phases else 0,
                format_func=lambda x: phase_descriptions.get(x, x)
            )
            
            if st.button("🔄 Update Phase"):
                if new_phase != current_phase:
                    result = set_automation_phase(new_phase)
                    if "error" in result:
                        st.error(f"Failed to update: {result['error']}")
                    else:
                        st.success(f"Phase updated to {new_phase}")
                        st.rerun()
        
        st.markdown("---")
        
        # Emergency Controls
        st.subheader("🚨 Emergency Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛑 EMERGENCY STOP", type="primary"):
                result = emergency_stop()
                if "error" in result:
                    st.error(f"Failed: {result['error']}")
                else:
                    st.success("Emergency stop activated!")
                    st.rerun()
        
        with col2:
            if st.button("🔄 Reset Stop"):
                result = reset_emergency()
                if "error" in result:
                    st.error(f"Failed: {result['error']}")
                else:
                    st.success("Emergency stop reset!")
                    st.rerun()
        
        st.markdown("---")
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto Refresh", value=True)
        refresh_interval = st.slider("Refresh Interval (seconds)", 5, 60, 10)
        
        if st.button("🔄 Refresh Now"):
            st.rerun()
        
        st.markdown("---")
        
        # Test signals
        st.subheader("🧪 Test Signals")
        test_symbol = st.selectbox("Symbol", ["EURUSD", "GBPUSD", "BTCUSDT"])
        test_price = st.number_input("Price", value=1.1000, step=0.0001, format="%.4f")
        
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
    # System Status Header
    health = get_bot_health()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if health.get("status") == "healthy":
            st.success("🟢 System Online")
        else:
            st.error("🔴 System Offline")
    
    with col2:
        automation_phase = health.get("automation_phase", "UNKNOWN")
        phase_colors = {
            "SIGNAL_ONLY": "🟡",
            "SEMI_AUTO": "🟠", 
            "FULL_AUTO": "🟢"
        }
        st.info(f"{phase_colors.get(automation_phase, '⚪')} {automation_phase}")
    
    with col3:
        emergency_stop_active = health.get("emergency_stop", False)
        if emergency_stop_active:
            st.error("🚨 Emergency Stop")
        else:
            st.success("✅ Normal Operation")
    
    with col4:
        daily_trades = health.get("daily_trades", 0)
        st.metric("Daily Trades", daily_trades, help="Trades executed today")
    
    with col5:
        daily_pnl = health.get("daily_pnl", 0)
        pnl_color = "normal" if daily_pnl >= 0 else "inverse"
        st.metric("Daily P&L", f"{daily_pnl:.2f}%", delta_color=pnl_color)
    
    st.markdown("---")
    
    # Get comprehensive status
    status = get_bot_status()
    
    if "error" in status:
        st.error(f"❌ Cannot connect to bot: {status['error']}")
        st.info("Make sure your bot is running on Railway and the URL is correct.")
        return
    
    # Profit Tracking Section
    st.header("💰 Profit & Withdrawal Tracker")
    
    profit_info = get_profit_info()
    if "error" not in profit_info:
        profit_tracker = profit_info.get("profit_tracker", {})
        withdrawal_rec = profit_info.get("withdrawal_recommendation", {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            starting_balance = profit_tracker.get("starting_balance", 0)
            st.metric("Starting Balance", f"${starting_balance:.2f}")
        
        with col2:
            current_balance = profit_tracker.get("current_balance", 0)
            total_profit = profit_tracker.get("total_profit", 0)
            st.metric("Current Balance", f"${current_balance:.2f}", f"${total_profit:.2f}")
        
        with col3:
            withdrawable = profit_tracker.get("withdrawable_profit", 0)
            st.metric("Withdrawable", f"${withdrawable:.2f}")
        
        with col4:
            total_return = (total_profit / starting_balance * 100) if starting_balance > 0 else 0
            st.metric("Total Return", f"{total_return:.2f}%")
        
        # Withdrawal Recommendation
        if withdrawal_rec.get("should_withdraw", False):
            st.success(f"💡 **Withdrawal Recommended:** ${withdrawal_rec.get('withdrawable_amount', 0):.2f}")
            st.info("Consider withdrawing profits to secure gains!")
        else:
            st.info("Continue trading - withdrawal not recommended yet")
    
    st.markdown("---")
    
    # Daily Performance
    st.header("📊 Daily Performance")
    
    daily_stats = status.get("daily_stats", {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        trades_today = daily_stats.get("trades", 0)
        st.metric("Trades Today", trades_today, help="Total trades executed today")
    
    with col2:
        win_rate = daily_stats.get("win_rate", 0)
        st.metric("Win Rate", f"{win_rate:.1f}%", help="Percentage of winning trades")
    
    with col3:
        wins = daily_stats.get("wins", 0)
        losses = daily_stats.get("losses", 0)
        st.metric("Wins/Losses", f"{wins}/{losses}")
    
    with col4:
        consecutive_losses = daily_stats.get("consecutive_losses", 0)
        if consecutive_losses >= 2:
            st.error(f"⚠️ {consecutive_losses} Consecutive Losses")
        else:
            st.metric("Consecutive Losses", consecutive_losses)
    
    # Risk Status
    st.subheader("🛡️ Risk Status")
    
    daily_pnl = daily_stats.get("pnl_percent", 0)
    max_daily_loss = -2.0  # 2% max loss
    max_trades = 5
    
    # Risk gauges
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily P&L gauge
        pnl_percentage = abs(daily_pnl / max_daily_loss * 100) if daily_pnl < 0 else 0
        
        if daily_pnl <= max_daily_loss:
            st.error(f"🚨 Daily Loss Limit Reached: {daily_pnl:.2f}%")
        elif daily_pnl <= max_daily_loss * 0.5:
            st.warning(f"⚠️ Approaching Loss Limit: {daily_pnl:.2f}%")
        else:
            st.success(f"✅ Daily P&L: {daily_pnl:.2f}%")
    
    with col2:
        # Trade count gauge
        trade_percentage = (trades_today / max_trades * 100) if max_trades > 0 else 0
        
        if trades_today >= max_trades:
            st.error(f"🚨 Daily Trade Limit Reached: {trades_today}/{max_trades}")
        elif trades_today >= max_trades * 0.8:
            st.warning(f"⚠️ Approaching Trade Limit: {trades_today}/{max_trades}")
        else:
            st.success(f"✅ Daily Trades: {trades_today}/{max_trades}")
    
    st.markdown("---")
    
    # Recent Trades
    st.header("📈 Recent Activity")
    
    recent_trades = status.get("recent_trades", [])
    if recent_trades:
        # Convert to DataFrame for better display
        trades_data = []
        for trade in recent_trades[-10:]:  # Last 10 activities
            trades_data.append({
                'Time': trade.get('timestamp', 'N/A')[:19].replace('T', ' '),
                'Action': trade.get('action', 'N/A'),
                'Symbol': trade.get('symbol', 'N/A'),
                'Price': f"${float(trade.get('price', 0)):.4f}" if trade.get('price') else 'N/A',
                'Status': trade.get('status', 'N/A'),
                'Reason': trade.get('reason', 'N/A'),
                'P&L %': f"{trade.get('profit_percent', 0):.3f}%" if 'profit_percent' in trade else 'N/A'
            })
        
        if trades_data:
            df_trades = pd.DataFrame(trades_data)
            st.dataframe(df_trades, use_container_width=True)
            
            # P&L Chart
            pnl_trades = [t for t in recent_trades if 'profit_percent' in t]
            if pnl_trades:
                st.subheader("📊 P&L Chart")
                
                cumulative_pnl = 0
                chart_data = []
                
                for i, trade in enumerate(pnl_trades):
                    cumulative_pnl += trade.get('profit_percent', 0)
                    chart_data.append({
                        'Trade': i + 1,
                        'Individual P&L': trade.get('profit_percent', 0),
                        'Cumulative P&L': cumulative_pnl
                    })
                
                if chart_data:
                    df_pnl = pd.DataFrame(chart_data)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df_pnl['Trade'],
                        y=df_pnl['Cumulative P&L'],
                        mode='lines+markers',
                        name='Cumulative P&L %',
                        line=dict(color='green' if df_pnl['Cumulative P&L'].iloc[-1] > 0 else 'red')
                    ))
                    
                    fig.update_layout(
                        title="Cumulative P&L Over Recent Trades",
                        xaxis_title="Trade Number",
                        yaxis_title="P&L (%)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No recent activity")
    
    # System Information
    with st.expander("🔍 System Information"):
        st.json({
            "Bot URL": BOT_URL,
            "System Type": "Profitable Trading System",
            "Focus": "Small wins, strict risk management",
            "Max Risk per Trade": "0.5-1%",
            "Max Daily Loss": "2%",
            "Trading Sessions": "London (8-12 GMT), NY (13-17 GMT)",
            "Strategy": "EMA pullback + RSI confirmation"
        })
    
    # Raw Status (for debugging)
    with st.expander("🔍 Raw Bot Status (Debug)"):
        st.json(status)
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()