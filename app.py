"""
Streamlit Trading Bot Dashboard
AI-Powered Trading Bot with Streamlit UI, yfinance data, and OpenAI integration.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from strategy_engine import StrategyEngine

# Page configuration
st.set_page_config(
    page_title="AI Trading Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'account_balance' not in st.session_state:
    st.session_state.account_balance = 10000.0

if 'buying_power' not in st.session_state:
    st.session_state.buying_power = 10000.0

if 'positions' not in st.session_state:
    st.session_state.positions = {}

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'logs' not in st.session_state:
    st.session_state.logs = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'strategy_engine' not in st.session_state:
    st.session_state.strategy_engine = StrategyEngine()

# Title
st.title("📈 AI Trading Bot Dashboard")

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")

# Trading symbols input
symbols_input = st.sidebar.text_input(
    "Trading Symbols (comma separated)",
    value="AAPL,AMZN",
    help="Enter stock symbols separated by commas"
)
symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]

# Levels input
levels = st.sidebar.number_input(
    "Levels",
    min_value=1,
    max_value=10,
    value=3,
    help="Number of trading levels"
)

# Drawdown percentage slider
drawdown_pct = st.sidebar.slider(
    "Drawdown %",
    min_value=1,
    max_value=20,
    value=5,
    help="Maximum drawdown percentage threshold"
)

st.sidebar.markdown("---")

# Main content area
col1, col2, col3 = st.columns(3)

# Account Status
with col1:
    st.metric("💰 Cash", f"${st.session_state.account_balance:,.2f}")

with col2:
    st.metric("⚡ Buying Power", f"${st.session_state.buying_power:,.2f}")

with col3:
    total_positions = len(st.session_state.positions)
    st.metric("📊 Open Positions", total_positions)

st.markdown("---")

# Tracked Equities Section
st.subheader("📋 Tracked Equities")

if symbols:
    equities_data = []
    
    for symbol in symbols:
        try:
            price = st.session_state.strategy_engine.get_current_price(symbol)
            if price:
                equities_data.append({
                    'Symbol': symbol,
                    'Latest Price': f"${price:.2f}",
                    'Action': symbol
                })
            else:
                equities_data.append({
                    'Symbol': symbol,
                    'Latest Price': "N/A",
                    'Action': symbol
                })
        except Exception as e:
            equities_data.append({
                'Symbol': symbol,
                'Latest Price': "Error",
                'Action': symbol
            })
    
    if equities_data:
        df_equities = pd.DataFrame(equities_data)
        
        # Display table without action column first
        st.dataframe(df_equities[['Symbol', 'Latest Price']], use_container_width=True)
        
        # Add buy order buttons
        st.markdown("**Quick Actions:**")
        cols = st.columns(len(symbols))
        for idx, symbol in enumerate(symbols):
            with cols[idx]:
                if st.button(f"📥 Buy {symbol}", key=f"buy_{symbol}"):
                    try:
                        price = st.session_state.strategy_engine.get_current_price(symbol)
                        if price:
                            # Place a buy order
                            result = st.session_state.strategy_engine.place_mock_trade(
                                symbol, 1, price, levels
                            )
                            if result:
                                st.success(f"Buy order placed for {symbol} at ${price:.2f}")
                                st.rerun()
                    except Exception as e:
                        st.error(f"Error placing order: {e}")
else:
    st.info("Enter trading symbols in the sidebar to track equities.")

st.markdown("---")

# Orders Section
st.subheader("📊 Orders")

if st.session_state.orders:
    # Convert orders to DataFrame
    orders_df = pd.DataFrame(st.session_state.orders)
    
    # Format the DataFrame for display
    display_orders = orders_df.copy()
    if 'timestamp' in display_orders.columns:
        display_orders['timestamp'] = pd.to_datetime(display_orders['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    if 'price' in display_orders.columns:
        display_orders['price'] = display_orders['price'].apply(lambda x: f"${x:.2f}")
    
    # Show most recent orders first
    display_orders = display_orders.iloc[::-1]
    
    st.dataframe(display_orders, use_container_width=True)
    
    if st.button("🗑️ Clear Orders"):
        st.session_state.orders = []
        st.rerun()
else:
    st.info("No orders yet. Place orders using the 'Place Buy Order' buttons above or 'Run Bot' below.")

st.markdown("---")

# AI Portfolio Manager Chat
st.subheader("🤖 AI Portfolio Manager")

chat_col1, chat_col2 = st.columns([3, 1])

with chat_col1:
    user_message = st.text_input("Ask the AI Portfolio Manager:", key="chat_input", 
                                 placeholder="E.g., 'What's your analysis of my current portfolio?'")

with chat_col2:
    st.write("")  # Spacing
    send_chat = st.button("💬 Send", use_container_width=True)

if send_chat and user_message:
    with st.spinner("Getting AI response..."):
        try:
            response = st.session_state.strategy_engine.chat_with_ai(user_message)
            st.session_state.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'user': user_message,
                'ai': response
            })
        except Exception as e:
            st.error(f"Error getting AI response: {e}")

# Display chat history
if st.session_state.chat_history:
    st.markdown("**Chat History:**")
    chat_container = st.container()
    with chat_container:
        # Show most recent chats first
        for chat in reversed(st.session_state.chat_history[-5:]):
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**AI:** {chat['ai']}")
            st.markdown("---")

st.markdown("---")

# System Logs
st.subheader("📝 System Logs / Recent Activity")

if st.session_state.logs:
    logs_df = pd.DataFrame(st.session_state.logs)
    
    # Format logs for display
    display_logs = logs_df.copy()
    if 'timestamp' in display_logs.columns:
        display_logs['timestamp'] = pd.to_datetime(display_logs['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    if 'price' in display_logs.columns:
        display_logs['price'] = display_logs['price'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
    if 'signal' in display_logs.columns:
        display_logs['signal'] = display_logs['signal'].apply(
            lambda x: "BUY" if x == 1 else "SELL" if x == -1 else "HOLD"
        )
    
    # Show most recent logs first
    display_logs = display_logs.iloc[::-1].head(10)
    
    st.dataframe(display_logs, use_container_width=True)
    
    if st.button("🗑️ Clear Logs"):
        st.session_state.logs = []
        st.rerun()
else:
    st.info("No activity logs yet. Run the bot to see trading activity.")

st.markdown("---")

# Run Bot Section
st.subheader("🚀 Run Trading Bot")

col_run1, col_run2, col_run3 = st.columns([2, 2, 1])

with col_run1:
    run_bot = st.button("▶️ Run Bot", type="primary", use_container_width=True)

with col_run2:
    stop_bot = st.button("⏹️ Stop Bot", use_container_width=True)

with col_run3:
    reset_account = st.button("🔄 Reset", use_container_width=True)

if run_bot:
    if not symbols:
        st.error("Please enter at least one trading symbol in the sidebar.")
    else:
        st.info("Running trading bot...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, symbol in enumerate(symbols):
            status_text.text(f"Processing {symbol}...")
            
            try:
                result = st.session_state.strategy_engine.run_strategy(
                    symbol, 
                    levels=levels, 
                    drawdown_pct=drawdown_pct
                )
                
                if result['success']:
                    st.success(f"✅ {symbol}: Signal={result.get('signal', 0)}, Price=${result.get('price', 0):.2f}")
                else:
                    st.warning(f"⚠️ {symbol}: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ {symbol}: Error - {e}")
            
            progress_bar.progress((idx + 1) / len(symbols))
        
        status_text.text("Bot run complete!")
        st.balloons()
        
        # Rerun to update all displays
        st.rerun()

if stop_bot:
    st.warning("Bot stopped.")

if reset_account:
    st.session_state.account_balance = 10000.0
    st.session_state.buying_power = 10000.0
    st.session_state.positions = {}
    st.session_state.orders = []
    st.session_state.logs = []
    st.session_state.chat_history = []
    st.success("Account reset to initial state.")
    st.rerun()

# Footer
st.markdown("---")
st.markdown("*AI Trading Bot powered by Streamlit, yfinance, and OpenAI*")
