#!/usr/bin/env python3
"""
Example: How to run a backtest without the full bot.
This script demonstrates backtesting with synthetic data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 70)
print("Forex Strategy Backtesting Example")
print("=" * 70)
print()

# Check if dependencies are available
try:
    import backtrader as bt
    print("✓ Backtrader is installed")
except ImportError:
    print("✗ Backtrader not installed. Run: pip install backtrader")
    exit(1)

try:
    from backtester import ForexBacktester
    print("✓ Backtester module loaded")
except ImportError as e:
    print(f"✗ Error loading backtester: {e}")
    exit(1)

print()
print("=" * 70)
print("Creating Synthetic OHLCV Data")
print("=" * 70)
print()

# Generate synthetic forex data (EUR/USD example)
# In real use, this data would come from OANDA via broker_connector
np.random.seed(42)

# Create 300 hourly candles (about 12.5 days)
num_candles = 300
start_date = datetime.now() - timedelta(hours=num_candles)
dates = pd.date_range(start=start_date, periods=num_candles, freq='1h')

# Generate price data with trends and noise
# Starting around 1.1000 (typical EUR/USD level)
base_price = 1.1000

# Create trending price movement
trend = np.linspace(0, 0.01, num_candles)  # Slight uptrend
noise = np.random.randn(num_candles) * 0.0005  # Random noise
prices = base_price + trend + noise

# Create OHLC data
# High is a bit above close, low is a bit below
df = pd.DataFrame({
    'open': prices - np.random.rand(num_candles) * 0.0003,
    'high': prices + np.random.rand(num_candles) * 0.0010,
    'low': prices - np.random.rand(num_candles) * 0.0010,
    'close': prices,
    'volume': np.random.randint(1000, 10000, num_candles)
}, index=dates)

# Ensure high is highest and low is lowest
df['high'] = df[['open', 'high', 'close']].max(axis=1)
df['low'] = df[['open', 'low', 'close']].min(axis=1)

print(f"Generated {len(df)} hourly candles")
print(f"Date range: {df.index[0]} to {df.index[-1]}")
print(f"Price range: {df['close'].min():.5f} to {df['close'].max():.5f}")
print()

print("Sample data (first 5 rows):")
print(df.head())
print()

print("=" * 70)
print("Running Backtest")
print("=" * 70)
print()

# Create backtester instance
backtester = ForexBacktester()

# Define backtest parameters
params = {
    'initial_cash': 10000.0,    # Starting capital
    'short_ma': 20,             # Short MA period (reduced for limited data)
    'long_ma': 50,              # Long MA period (reduced for limited data)
    'risk_per_trade': 0.01,     # 1% risk per trade
    'stop_loss_pct': 0.01,      # 1% stop-loss
    'take_profit_pct': 0.02     # 2% take-profit
}

print("Backtest Parameters:")
for key, value in params.items():
    print(f"  {key}: {value}")
print()

# Run the backtest
try:
    results = backtester.run_backtest(df, **params)
    
    print()
    print("=" * 70)
    print("Backtest Completed!")
    print("=" * 70)
    print()
    
    # Print detailed results
    backtester.print_results()
    
    # Analysis
    print("=" * 70)
    print("Performance Analysis")
    print("=" * 70)
    print()
    
    # Calculate additional metrics
    roi = results['return_pct']
    sharpe = results['sharpe_ratio']
    max_dd = results['max_drawdown']
    win_rate = results['win_rate']
    
    print("Rating:")
    if roi > 10 and sharpe > 1 and win_rate > 50:
        print("  ⭐⭐⭐ Excellent performance!")
    elif roi > 5 and sharpe > 0.5 and win_rate > 45:
        print("  ⭐⭐ Good performance")
    elif roi > 0:
        print("  ⭐ Positive returns")
    else:
        print("  ✗ Needs improvement")
    
    print()
    print("Recommendations:")
    if max_dd > 15:
        print("  ⚠️  High drawdown - consider reducing position size")
    if win_rate < 40:
        print("  ⚠️  Low win rate - review entry signals")
    if sharpe < 0.5:
        print("  ⚠️  Low risk-adjusted returns - optimize parameters")
    if results['total_trades'] < 5:
        print("  ℹ️  Few trades - consider longer backtest period or different parameters")
    
    if max_dd <= 15 and win_rate >= 45 and sharpe >= 0.5:
        print("  ✓ Strategy shows promise - consider paper trading next")
    
    print()
    
except Exception as e:
    print(f"✗ Backtest failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("=" * 70)
print("Next Steps")
print("=" * 70)
print()
print("1. Try different strategy parameters:")
print("   - Adjust MA periods (10/20, 20/50, 50/200)")
print("   - Change risk/reward ratios")
print("   - Test different timeframes")
print()
print("2. Test with real historical data:")
print("   - Use broker_connector to fetch OANDA data")
print("   - Backtest on 6+ months of data")
print("   - Test on different currency pairs")
print()
print("3. Validate results:")
print("   - Run multiple backtests with different periods")
print("   - Check performance in trending vs ranging markets")
print("   - Verify results are consistent")
print()
print("4. Paper trade before going live:")
print("   - Use OANDA practice account")
print("   - Run for at least 1 month")
print("   - Compare to backtest results")
print()

print("=" * 70)
print("Happy backtesting! 📊")
print("=" * 70)
