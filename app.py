#!/usr/bin/env python3
"""
Streamlit Dashboard for Forex Trading Bot
Replaces the Tkinter GUI with a modern web-based interface.
"""
import streamlit as st
import pandas as pd
import time
import threading
from datetime import datetime
from forex_bot import ForexTradingBot

# Page config
st.set_page_config(
    page_title="AI Forex Trading Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def init_session_state():
    """Initialize Streamlit session state variables."""
    if 'bot' not in st.session_state:
        st.session_state.bot = ForexTradingBot()
        st.session_state.bot.initialize_components()
    
    if 'bot_running' not in st.session_state:
        st.session_state.bot_running = False
    
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()

def log_message(message):
    """Add a log message with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.session_state.logs.append(f"[{timestamp}] {message}")
    # Keep only last 100 logs
    if len(st.session_state.logs) > 100:
        st.session_state.logs = st.session_state.logs[-100:]

def setup_sidebar():
    """Setup the configuration sidebar."""
    st.sidebar.title("⚙️ Configuration")
    
    st.sidebar.subheader("Trading Pairs")
    pairs_input = st.sidebar.text_input(
        "Pairs (comma-separated)",
        value="EUR/USD,GBP/USD,USD/JPY",
        help="Enter trading pairs separated by commas"
    )
    
    st.sidebar.subheader("Strategy Parameters")
    short_ma = st.sidebar.number_input(
        "Short MA Period",
        min_value=10,
        max_value=500,
        value=50,
        step=10
    )
    
    long_ma = st.sidebar.number_input(
        "Long MA Period",
        min_value=50,
        max_value=500,
        value=200,
        step=10
    )
    
    timeframe = st.sidebar.selectbox(
        "Timeframe",
        options=["5m", "15m", "30m", "1h", "4h", "1d"],
        index=3
    )
    
    st.sidebar.subheader("Risk Management")
    risk_per_trade = st.sidebar.number_input(
        "Risk per Trade (%)",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1
    )
    
    stop_loss = st.sidebar.number_input(
        "Stop Loss (%)",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1
    )
    
    take_profit = st.sidebar.number_input(
        "Take Profit (%)",
        min_value=0.1,
        max_value=20.0,
        value=2.0,
        step=0.1
    )
    
    max_drawdown = st.sidebar.slider(
        "Max Drawdown (%)",
        min_value=1.0,
        max_value=50.0,
        value=10.0,
        step=1.0
    )
    
    st.sidebar.divider()
    
    # Control buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("▶️ Start Bot", disabled=st.session_state.bot_running, use_container_width=True):
            config = {
                'pairs': [p.strip() for p in pairs_input.split(',')],
                'short_ma': int(short_ma),
                'long_ma': int(long_ma),
                'timeframe': timeframe,
                'risk_per_trade': float(risk_per_trade) / 100,
                'stop_loss_pct': float(stop_loss) / 100,
                'take_profit_pct': float(take_profit) / 100,
                'max_drawdown': float(max_drawdown) / 100
            }
            
            # Start bot in thread
            threading.Thread(
                target=st.session_state.bot.start,
                args=(config,),
                daemon=True
            ).start()
            
            st.session_state.bot_running = True
            log_message("Bot started with configuration")
            st.success("Bot started!")
            st.rerun()
    
    with col2:
        if st.button("⏹️ Stop Bot", disabled=not st.session_state.bot_running, use_container_width=True):
            st.session_state.bot.stop()
            st.session_state.bot_running = False
            log_message("Bot stopped by user")
            st.warning("Bot stopped!")
            st.rerun()
    
    if st.sidebar.button("💾 Save Config", use_container_width=True):
        config = {
            'pairs': [p.strip() for p in pairs_input.split(',')],
            'short_ma': int(short_ma),
            'long_ma': int(long_ma),
            'timeframe': timeframe,
            'risk_per_trade': float(risk_per_trade) / 100,
            'stop_loss_pct': float(stop_loss) / 100,
            'take_profit_pct': float(take_profit) / 100,
            'max_drawdown': float(max_drawdown) / 100
        }
        st.session_state.bot.save_configuration(config)
        log_message("Configuration saved")
        st.sidebar.success("Configuration saved!")

def display_account_overview():
    """Display account overview metrics."""
    st.header("📊 Account Overview")
    
    # Get dashboard data from bot
    dashboard_data = st.session_state.bot.get_dashboard_data()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Balance",
            value=f"${dashboard_data['balance']:.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Open Positions",
            value=dashboard_data['positions_count']
        )
    
    with col3:
        pnl = dashboard_data['daily_pnl']
        st.metric(
            label="Daily P&L",
            value=f"${pnl:.2f}",
            delta=f"{pnl:+.2f}"
        )
    
    with col4:
        status = "🟢 Running" if st.session_state.bot_running else "🔴 Stopped"
        st.metric(label="Status", value=status)

def display_positions():
    """Display open positions table."""
    st.subheader("💼 Open Positions")
    
    dashboard_data = st.session_state.bot.get_dashboard_data()
    
    if dashboard_data['positions']:
        df = pd.DataFrame(
            dashboard_data['positions'],
            columns=['Symbol', 'Side', 'Size', 'Entry', 'Current', 'P&L']
        )
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No open positions")

def display_recent_trades():
    """Display recent trades table."""
    st.subheader("📋 Recent Trades")
    
    dashboard_data = st.session_state.bot.get_dashboard_data()
    
    if dashboard_data['recent_trades']:
        df = pd.DataFrame(
            dashboard_data['recent_trades'],
            columns=['Time', 'Symbol', 'Side', 'Size', 'Entry', 'Exit', 'P&L']
        )
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No recent trades")

def display_ai_chat():
    """Display AI Portfolio Manager chat interface."""
    st.subheader("🤖 AI Portfolio Manager")
    
    # Quick action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Analyze Portfolio", use_container_width=True):
            quick_query("Analyze my current portfolio")
    
    with col2:
        if st.button("⚠️ Risk Assessment", use_container_width=True):
            quick_query("Assess the risk of my positions")
    
    with col3:
        if st.button("💡 Suggestions", use_container_width=True):
            quick_query("What are your suggestions for my trading?")
    
    # Chat history display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.chat_message("user").write(msg['content'])
            else:
                st.chat_message("assistant").write(msg['content'])
    
    # Chat input
    if prompt := st.chat_input("Ask the AI assistant..."):
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': prompt
        })
        
        # Display user message
        st.chat_message("user").write(prompt)
        
        # Get AI response
        with st.spinner("AI is thinking..."):
            response = st.session_state.bot.query_ai(prompt)
        
        # Add and display AI response
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })
        st.chat_message("assistant").write(response)
        
        log_message(f"AI query: {prompt[:50]}...")
        st.rerun()

def quick_query(query):
    """Send a quick query to AI."""
    # Add user message
    st.session_state.chat_history.append({
        'role': 'user',
        'content': query
    })
    
    # Get AI response
    response = st.session_state.bot.query_ai(query)
    
    # Add AI response
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': response
    })
    
    log_message(f"Quick query: {query[:50]}...")
    st.rerun()

def display_logs():
    """Display system logs."""
    with st.expander("📝 System Logs", expanded=False):
        col1, col2 = st.columns([5, 1])
        
        with col2:
            if st.button("Clear Logs"):
                st.session_state.logs = []
                st.rerun()
        
        if st.session_state.logs:
            logs_text = "\n".join(st.session_state.logs[-50:])  # Show last 50 logs
            st.text_area(
                "Recent Activity",
                value=logs_text,
                height=200,
                disabled=True,
                label_visibility="collapsed"
            )
        else:
            st.info("No logs yet")

def main():
    """Main Streamlit app."""
    # Initialize session state
    init_session_state()
    
    # Title
    st.title("🤖 AI-Powered Forex Trading Bot")
    
    # Sidebar configuration
    setup_sidebar()
    
    # Main content area
    display_account_overview()
    
    st.divider()
    
    # Two columns for positions and trades
    col1, col2 = st.columns(2)
    
    with col1:
        display_positions()
    
    with col2:
        display_recent_trades()
    
    st.divider()
    
    # AI Chat
    display_ai_chat()
    
    st.divider()
    
    # Logs
    display_logs()
    
    # Auto-refresh (every 5 seconds when bot is running)
    if st.session_state.bot_running:
        time.sleep(0.1)  # Small delay to prevent too frequent updates
        if time.time() - st.session_state.last_update > 5:
            st.session_state.last_update = time.time()
            st.rerun()

if __name__ == "__main__":
    main()
