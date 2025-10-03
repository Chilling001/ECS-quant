#!/usr/bin/env python3
"""
Module Usage Examples
Demonstrates how to use each module independently.
"""

print("=" * 70)
print("Forex Bot - Module Usage Examples")
print("=" * 70)
print()

# =============================================================================
# EXAMPLE 1: Using the Strategy Module
# =============================================================================
print("=" * 70)
print("EXAMPLE 1: Using the Strategy Module")
print("=" * 70)
print()

print("The strategy module calculates signals and manages risk.\n")

print("Code:")
print("-" * 70)
print("""
from forex_strategy import MovingAverageCrossoverStrategy

# Create strategy
strategy = MovingAverageCrossoverStrategy(
    short_ma=50,
    long_ma=200,
    risk_per_trade=0.01,    # 1% risk
    stop_loss_pct=0.01,     # 1% SL
    take_profit_pct=0.02    # 2% TP
)

# Calculate stop-loss and take-profit
entry_price = 1.10000
stop_loss = strategy.calculate_stop_loss(entry_price, 'long')
take_profit = strategy.calculate_take_profit(entry_price, 'long')

print(f"Entry: {entry_price:.5f}")
print(f"Stop Loss: {stop_loss:.5f}")
print(f"Take Profit: {take_profit:.5f}")

# Calculate position size
balance = 10000
position_size = strategy.calculate_position_size(balance, entry_price, stop_loss)
print(f"Position Size: {position_size:.2f} units")
""")
print("-" * 70)
print()

# =============================================================================
# EXAMPLE 2: Using the Broker Connector
# =============================================================================
print("=" * 70)
print("EXAMPLE 2: Using the Broker Connector")
print("=" * 70)
print()

print("Connect to OANDA and fetch market data.\n")

print("Code:")
print("-" * 70)
print("""
from broker_connector import OANDAConnector
import config

# Initialize connector
broker = OANDAConnector(
    api_key=config.OANDA_API_KEY,
    account_id=config.OANDA_ACCOUNT_ID,
    practice=True  # Paper trading
)

# Get account balance
balance = broker.get_balance()
print(f"Balance: ${balance['total']:.2f}")

# Fetch historical data
df = broker.get_ohlcv('EUR/USD', '1h', limit=100)
print(f"Fetched {len(df)} candles")

# Get current price
ticker = broker.get_ticker('EUR/USD')
print(f"Current EUR/USD: {ticker['last']:.5f}")

# Place an order (careful!)
order = broker.create_market_order('EUR/USD', 'buy', 1000)
""")
print("-" * 70)
print()

# =============================================================================
# EXAMPLE 3: Using the AI Manager
# =============================================================================
print("=" * 70)
print("EXAMPLE 3: Using the AI Manager")
print("=" * 70)
print()

print("Get AI-powered portfolio analysis and advice.\n")

print("Code:")
print("-" * 70)
print("""
from ai_manager import AIPortfolioManager
import config

# Initialize AI manager
ai = AIPortfolioManager(config.OPENAI_API_KEY)

# Get portfolio analysis
account_info = broker.get_account_info()
positions = broker.get_positions()
recent_trades = []

analysis = ai.analyze_portfolio(account_info, positions, recent_trades)
print(analysis)

# Ask a question
response = ai.chat_query("What's a good risk/reward ratio for forex?")
print(response)

# Evaluate a trade idea
evaluation = ai.evaluate_trade_idea(
    symbol='EUR/USD',
    side='buy',
    entry_price=1.10000,
    account_balance=10000,
    current_positions=positions
)
print(evaluation)
""")
print("-" * 70)
print()

# =============================================================================
# EXAMPLE 4: Using the Telegram Notifier
# =============================================================================
print("=" * 70)
print("EXAMPLE 4: Using the Telegram Notifier")
print("=" * 70)
print()

print("Send trading notifications to Telegram.\n")

print("Code:")
print("-" * 70)
print("""
from telegram_notifier import TelegramNotifier
import config

# Initialize notifier
telegram = TelegramNotifier(
    config.TELEGRAM_BOT_TOKEN,
    config.TELEGRAM_CHAT_ID
)

# Send trade entry notification
telegram.send_trade_entry(
    symbol='EUR/USD',
    side='buy',
    amount=1000,
    entry_price=1.10000,
    stop_loss=1.09000,
    take_profit=1.12000
)

# Send trade exit notification
telegram.send_trade_exit(
    symbol='EUR/USD',
    side='buy',
    amount=1000,
    exit_price=1.11500,
    pnl=150.00
)

# Send alert
telegram.send_alert('warning', 'High volatility detected!')

# Send AI insight
telegram.send_ai_insight('Consider taking profits on EUR/USD position.')
""")
print("-" * 70)
print()

# =============================================================================
# EXAMPLE 5: Using the Backtester
# =============================================================================
print("=" * 70)
print("EXAMPLE 5: Using the Backtester")
print("=" * 70)
print()

print("Backtest strategies on historical data.\n")

print("Code:")
print("-" * 70)
print("""
from backtester import ForexBacktester

# Fetch historical data
df = broker.get_ohlcv('EUR/USD', '1h', limit=500)

# Create backtester
backtester = ForexBacktester()

# Run backtest
results = backtester.run_backtest(
    data_df=df,
    initial_cash=10000,
    short_ma=50,
    long_ma=200,
    risk_per_trade=0.01,
    stop_loss_pct=0.01,
    take_profit_pct=0.02
)

# Print results
backtester.print_results()

# Get specific metrics
print(f"Return: {results['return_pct']:.2f}%")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.3f}")
print(f"Win Rate: {results['win_rate']:.2f}%")
""")
print("-" * 70)
print()

# =============================================================================
# EXAMPLE 6: Complete Trading Workflow
# =============================================================================
print("=" * 70)
print("EXAMPLE 6: Complete Trading Workflow")
print("=" * 70)
print()

print("Combining all modules for automated trading.\n")

print("Code:")
print("-" * 70)
print("""
# 1. Initialize all components
broker = OANDAConnector(api_key, account_id, practice=True)
strategy = MovingAverageCrossoverStrategy()
ai = AIPortfolioManager(openai_key)
telegram = TelegramNotifier(bot_token, chat_id)

# 2. Fetch market data
df = broker.get_ohlcv('EUR/USD', '1h', limit=250)

# 3. Calculate indicators and get signal
df = strategy.calculate_indicators(df)
signal = strategy.get_current_signal(df)

# 4. If buy signal, evaluate with AI
if signal == 1:
    current_price = df['close'].iloc[-1]
    balance = broker.get_balance()['total']
    positions = broker.get_positions()
    
    # Get AI evaluation
    evaluation = ai.evaluate_trade_idea(
        'EUR/USD', 'buy', current_price, balance, positions
    )
    print(f"AI Evaluation: {evaluation}")
    
    # If AI approves, execute trade
    if 'approve' in evaluation.lower():
        # Calculate position size and risk
        stop_loss = strategy.calculate_stop_loss(current_price, 'long')
        take_profit = strategy.calculate_take_profit(current_price, 'long')
        position_size = strategy.calculate_position_size(
            balance, current_price, stop_loss
        )
        
        # Place order
        order = broker.create_market_order('EUR/USD', 'buy', position_size)
        
        # Send notification
        telegram.send_trade_entry(
            'EUR/USD', 'buy', position_size,
            current_price, stop_loss, take_profit
        )
        
        print("Trade executed successfully!")

# 5. Monitor and manage positions
positions = broker.get_positions()
for symbol, pos in positions.items():
    # Check exit conditions
    df = broker.get_ohlcv(symbol, '1h', limit=250)
    df = strategy.calculate_indicators(df)
    
    should_exit, reason = strategy.check_exit_conditions(
        df, pos['entryPrice'], pos['side']
    )
    
    if should_exit:
        broker.close_position(symbol)
        telegram.send_alert('info', f'Closed {symbol}: {reason}')
""")
print("-" * 70)
print()

print("=" * 70)
print("Tips for Using These Examples")
print("=" * 70)
print()
print("1. Start by testing individual modules")
print("2. Use print() statements to understand data flow")
print("3. Test with paper trading (practice=True)")
print("4. Handle errors with try/except blocks")
print("5. Log all actions for debugging")
print("6. Test backtests before live trading")
print("7. Start with small position sizes")
print()

print("=" * 70)
print("For complete implementation, see: forex_bot.py")
print("=" * 70)
print()
