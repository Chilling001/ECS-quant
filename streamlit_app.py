"""
Streamlit Web Dashboard for Forex Trading Bot
Modern web interface replacing the Tkinter GUI.
"""
import streamlit as st
import pandas as pd
import time
from datetime import datetime
import threading
import os

# Import bot components
from forex_bot import ForexTradingBot

# Page configuration
st.set_page_config(
    page_title="AI Forex Trading Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .metric-positive {
        color: #00ff00;
    }
    .metric-negative {
        color: #ff0000;
    }
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize session state
if 'bot' not in st.session_state:
    st.session_state.bot = ForexTradingBot()
    st.session_state.bot_initialized = False
    st.session_state.bot_running = False
    st.session_state.chat_history = []
    st.session_state.logs = []

bot = st.session_state.bot


def log_message(message):
    """Add a log message with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    st.session_state.logs.append(log_entry)
    # Keep only last 100 logs
    if len(st.session_state.logs) > 100:
        st.session_state.logs = st.session_state.logs[-100:]


def initialize_bot():
    """Initialize bot components."""
    if not st.session_state.bot_initialized:
        with st.spinner("Initializing bot components..."):
            success = bot.initialize_components()
            st.session_state.bot_initialized = success
            if success:
                log_message("Bot components initialized successfully")
                st.success("✓ Bot initialized successfully!")
            else:
                log_message("Failed to initialize bot components")
                st.error("✗ Failed to initialize. Check your configuration.")
            return success
    return True


# Sidebar navigation
st.sidebar.title("📈 Forex Bot Dashboard")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Configuration", "AI Assistant", "Logs"]
)

# Sidebar status
st.sidebar.markdown("---")
st.sidebar.subheader("Bot Status")
if st.session_state.bot_running:
    st.sidebar.success("🟢 Running")
else:
    st.sidebar.info("🔴 Stopped")

st.sidebar.markdown("---")

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
if page == "Dashboard":
    st.title("📊 Trading Dashboard")
    
    # Initialize bot if not already done
    if not st.session_state.bot_initialized:
        st.info("Bot not initialized. Please configure and start the bot.")
        if st.button("Initialize Bot"):
            initialize_bot()
    
    # Get dashboard data
    dashboard_data = bot.get_dashboard_data()
    
    # Account Information
    st.subheader("Account Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        balance = dashboard_data.get('balance', 0)
        st.metric("Balance", f"${balance:,.2f}")
    
    with col2:
        positions_count = dashboard_data.get('positions_count', 0)
        st.metric("Open Positions", positions_count)
    
    with col3:
        daily_pnl = dashboard_data.get('daily_pnl', 0)
        pnl_color = "normal" if daily_pnl >= 0 else "inverse"
        st.metric("Daily P&L", f"${daily_pnl:,.2f}", delta=f"{daily_pnl:,.2f}", delta_color=pnl_color)
    
    st.markdown("---")
    
    # Open Positions
    st.subheader("Open Positions")
    positions = dashboard_data.get('positions', [])
    
    if positions:
        df_positions = pd.DataFrame(
            positions,
            columns=['Symbol', 'Side', 'Size', 'Entry', 'Current', 'P&L']
        )
        st.dataframe(df_positions, use_container_width=True)
    else:
        st.info("No open positions")
    
    st.markdown("---")
    
    # Recent Trades
    st.subheader("Recent Trades")
    trades = dashboard_data.get('recent_trades', [])
    
    if trades:
        df_trades = pd.DataFrame(
            trades,
            columns=['Time', 'Symbol', 'Side', 'Size', 'Entry', 'Exit', 'P&L']
        )
        st.dataframe(df_trades, use_container_width=True)
    else:
        st.info("No recent trades")
    
    # Auto-refresh
    if st.session_state.bot_running:
        st.caption("Dashboard updates automatically every 5 seconds")
        time.sleep(5)
        st.rerun()

# ============================================================================
# CONFIGURATION PAGE
# ============================================================================
elif page == "Configuration":
    st.title("⚙️ Bot Configuration")
    
    # Get current config or defaults
    current_config = bot.get_default_config()
    
    st.subheader("Trading Parameters")
    
    # Trading pairs
    pairs_input = st.text_input(
        "Trading Pairs (comma-separated)",
        value=",".join(current_config.get('pairs', ['EUR/USD', 'GBP/USD', 'USD/JPY']))
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        short_ma = st.number_input(
            "Short MA Period",
            min_value=1,
            max_value=500,
            value=current_config.get('short_ma', 50)
        )
        
        long_ma = st.number_input(
            "Long MA Period",
            min_value=1,
            max_value=500,
            value=current_config.get('long_ma', 200)
        )
        
        timeframe = st.selectbox(
            "Timeframe",
            ["5m", "15m", "30m", "1h", "4h", "1d"],
            index=3  # Default to 1h
        )
    
    with col2:
        risk_per_trade = st.number_input(
            "Risk per Trade (%)",
            min_value=0.1,
            max_value=10.0,
            value=current_config.get('risk_per_trade', 0.01) * 100,
            step=0.1
        )
        
        stop_loss_pct = st.number_input(
            "Stop Loss (%)",
            min_value=0.1,
            max_value=10.0,
            value=current_config.get('stop_loss_pct', 0.01) * 100,
            step=0.1
        )
        
        take_profit_pct = st.number_input(
            "Take Profit (%)",
            min_value=0.1,
            max_value=20.0,
            value=current_config.get('take_profit_pct', 0.02) * 100,
            step=0.1
        )
    
    max_drawdown = st.number_input(
        "Max Drawdown (%)",
        min_value=1.0,
        max_value=50.0,
        value=current_config.get('max_drawdown', 0.10) * 100,
        step=1.0
    )
    
    st.markdown("---")
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Configuration", use_container_width=True):
            config = {
                'pairs': [p.strip() for p in pairs_input.split(',')],
                'short_ma': int(short_ma),
                'long_ma': int(long_ma),
                'timeframe': timeframe,
                'risk_per_trade': risk_per_trade / 100,
                'stop_loss_pct': stop_loss_pct / 100,
                'take_profit_pct': take_profit_pct / 100,
                'max_drawdown': max_drawdown / 100
            }
            bot.save_configuration(config)
            log_message("Configuration saved")
            st.success("✓ Configuration saved successfully!")
    
    with col2:
        if st.button("▶️ Start Bot", use_container_width=True, disabled=st.session_state.bot_running):
            if not st.session_state.bot_initialized:
                initialize_bot()
            
            if st.session_state.bot_initialized:
                config = {
                    'pairs': [p.strip() for p in pairs_input.split(',')],
                    'short_ma': int(short_ma),
                    'long_ma': int(long_ma),
                    'timeframe': timeframe,
                    'risk_per_trade': risk_per_trade / 100,
                    'stop_loss_pct': stop_loss_pct / 100,
                    'take_profit_pct': take_profit_pct / 100,
                    'max_drawdown': max_drawdown / 100
                }
                
                # Start bot in separate thread
                threading.Thread(target=bot.start, args=(config,), daemon=True).start()
                st.session_state.bot_running = True
                log_message("Bot started")
                st.success("✓ Bot started!")
                time.sleep(1)
                st.rerun()
    
    with col3:
        if st.button("⏹️ Stop Bot", use_container_width=True, disabled=not st.session_state.bot_running):
            bot.stop()
            st.session_state.bot_running = False
            log_message("Bot stopped")
            st.success("✓ Bot stopped!")
            time.sleep(1)
            st.rerun()
    
    # Configuration info
    st.markdown("---")
    st.info("""
    **Configuration Tips:**
    - Start with conservative settings (low risk, tight stops)
    - Test with OANDA practice account before going live
    - Monitor the bot regularly and adjust as needed
    - Use stop losses on every trade
    """)

# ============================================================================
# AI ASSISTANT PAGE
# ============================================================================
elif page == "AI Assistant":
    st.title("🤖 AI Trading Assistant")
    
    # Check if AI is available
    if not bot.ai_manager:
        st.warning("⚠️ AI Manager not initialized. Check your OpenAI API key configuration.")
    else:
        st.info("Ask questions about your portfolio, trading strategy, or get market insights.")
    
    # Quick action buttons
    st.subheader("Quick Queries")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Analyze Portfolio"):
            query = "Analyze my current portfolio and positions"
            st.session_state.chat_history.append({"role": "user", "content": query})
    
    with col2:
        if st.button("⚠️ Risk Assessment"):
            query = "Assess the risk of my current positions"
            st.session_state.chat_history.append({"role": "user", "content": query})
    
    with col3:
        if st.button("💡 Get Suggestions"):
            query = "What are your suggestions for my trading strategy?"
            st.session_state.chat_history.append({"role": "user", "content": query})
    
    st.markdown("---")
    
    # Chat history
    st.subheader("Chat History")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**AI:** {msg['content']}")
            st.markdown("")
    
    # Process pending queries
    if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
        with st.spinner("AI is thinking..."):
            try:
                user_message = st.session_state.chat_history[-1]["content"]
                response = bot.query_ai(user_message)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                log_message(f"AI query: {user_message[:50]}...")
                st.rerun()
            except Exception as e:
                error_msg = f"Error getting AI response: {str(e)}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                log_message(error_msg)
                st.rerun()
    
    # Chat input
    st.markdown("---")
    user_input = st.text_input("Your question:", key="chat_input")
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Send", use_container_width=True):
            if user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# ============================================================================
# LOGS PAGE
# ============================================================================
elif page == "Logs":
    st.title("📋 System Logs")
    
    # Display logs
    if st.session_state.logs:
        st.text_area(
            "Log Output",
            value="\n".join(st.session_state.logs),
            height=500,
            disabled=True
        )
    else:
        st.info("No logs yet. Logs will appear here as the bot operates.")
    
    # Clear logs button
    if st.button("🗑️ Clear Logs"):
        st.session_state.logs = []
        st.rerun()
    
    # Export logs button
    if st.button("💾 Export Logs"):
        log_text = "\n".join(st.session_state.logs)
        st.download_button(
            label="Download Logs",
            data=log_text,
            file_name=f"forex_bot_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "AI-Powered Forex Trading Bot\n\n"
    "Modern web dashboard built with Streamlit"
)
