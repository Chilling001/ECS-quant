#!/usr/bin/env python3
"""
Simple test script to verify basic functionality of forex bot modules.
Tests module imports and basic instantiation without requiring API keys.
"""

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        import broker_connector
        print("✓ broker_connector imported")
    except Exception as e:
        print(f"✗ broker_connector failed: {e}")
    
    try:
        import forex_strategy
        print("✓ forex_strategy imported")
    except Exception as e:
        print(f"✗ forex_strategy failed: {e}")
    
    try:
        import ai_manager
        print("✓ ai_manager imported")
    except Exception as e:
        print(f"✗ ai_manager failed: {e}")
    
    try:
        import telegram_notifier
        print("✓ telegram_notifier imported")
    except Exception as e:
        print(f"✗ telegram_notifier failed: {e}")
    
    try:
        import backtester
        print("✓ backtester imported")
    except Exception as e:
        print(f"✗ backtester failed: {e}")
    
    try:
        import forex_gui
        print("✓ forex_gui imported")
    except Exception as e:
        print(f"✗ forex_gui failed: {e}")
    
    try:
        import forex_bot
        print("✓ forex_bot imported")
    except Exception as e:
        print(f"✗ forex_bot failed: {e}")
    
    print()

def test_strategy():
    """Test strategy module."""
    print("Testing forex strategy...")
    
    try:
        from forex_strategy import MovingAverageCrossoverStrategy
        
        # Create strategy instance
        strategy = MovingAverageCrossoverStrategy(
            short_ma=50,
            long_ma=200,
            risk_per_trade=0.01,
            stop_loss_pct=0.01,
            take_profit_pct=0.02
        )
        
        print(f"✓ Strategy created: {strategy.get_strategy_summary()}")
        
        # Test stop loss calculation
        entry = 1.1000
        sl = strategy.calculate_stop_loss(entry, 'long')
        print(f"✓ Stop loss for entry {entry}: {sl:.5f}")
        
        # Test take profit calculation
        tp = strategy.calculate_take_profit(entry, 'long')
        print(f"✓ Take profit for entry {entry}: {tp:.5f}")
        
        # Test position size calculation
        balance = 10000
        stop_loss = 1.0900
        size = strategy.calculate_position_size(balance, entry, stop_loss)
        print(f"✓ Position size for $10,000 balance: {size:.2f} units")
        
    except Exception as e:
        print(f"✗ Strategy test failed: {e}")
    
    print()

def test_backtester():
    """Test backtester with sample data."""
    print("Testing backtester...")
    
    try:
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        from backtester import ForexBacktester
        
        # Create sample OHLCV data
        dates = pd.date_range(start='2023-01-01', periods=300, freq='1h')
        
        # Generate synthetic price data with a trend
        np.random.seed(42)
        prices = 1.1000 + np.cumsum(np.random.randn(300) * 0.0002)
        
        df = pd.DataFrame({
            'open': prices,
            'high': prices + np.random.rand(300) * 0.0010,
            'low': prices - np.random.rand(300) * 0.0010,
            'close': prices + np.random.randn(300) * 0.0005,
            'volume': np.random.randint(1000, 10000, 300)
        }, index=dates)
        
        print(f"✓ Sample data created: {len(df)} candles")
        
        # Run backtest
        backtester = ForexBacktester()
        results = backtester.run_backtest(
            df,
            initial_cash=10000,
            short_ma=20,  # Use shorter periods for limited data
            long_ma=50,
            risk_per_trade=0.01,
            stop_loss_pct=0.01,
            take_profit_pct=0.02
        )
        
        print(f"✓ Backtest completed:")
        print(f"  - Initial: ${results['initial_value']:.2f}")
        print(f"  - Final: ${results['final_value']:.2f}")
        print(f"  - Return: {results['return_pct']:.2f}%")
        print(f"  - Total Trades: {results['total_trades']}")
        
    except Exception as e:
        print(f"✗ Backtester test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()

def test_telegram():
    """Test telegram notifier structure."""
    print("Testing telegram notifier...")
    
    try:
        from telegram_notifier import TelegramNotifier
        
        # Create notifier with dummy credentials (won't send)
        notifier = TelegramNotifier("dummy_token", "dummy_chat_id")
        
        print("✓ Telegram notifier created")
        print("  Note: Actual sending requires valid credentials")
        
    except Exception as e:
        print(f"✗ Telegram notifier test failed: {e}")
    
    print()

def main():
    """Run all tests."""
    print("=" * 60)
    print("Forex Trading Bot - Module Tests")
    print("=" * 60)
    print()
    
    test_imports()
    test_strategy()
    test_backtester()
    test_telegram()
    
    print("=" * 60)
    print("Testing complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Copy config_template.py to config.py")
    print("2. Fill in your API keys")
    print("3. Run: python forex_bot.py")

if __name__ == '__main__':
    main()
