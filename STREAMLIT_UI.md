# Streamlit Dashboard UI Overview

This document provides a textual representation of the Streamlit web dashboard layout.

## Application Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📈 Forex Bot Dashboard                                     [Settings]  │
├─────────────────┬───────────────────────────────────────────────────────┤
│                 │                                                       │
│  SIDEBAR        │  MAIN CONTENT AREA                                   │
│                 │                                                       │
│  Navigation     │  [Current Page Content]                              │
│  ○ Dashboard    │                                                       │
│  ○ Config       │                                                       │
│  ○ AI Assistant │                                                       │
│  ○ Logs         │                                                       │
│                 │                                                       │
│  ───────────    │                                                       │
│  Bot Status     │                                                       │
│  🟢 Running     │                                                       │
│  (or 🔴 Stop)   │                                                       │
│  ───────────    │                                                       │
│                 │                                                       │
│  About          │                                                       │
│  AI-Powered     │                                                       │
│  Forex Trading  │                                                       │
│  Bot            │                                                       │
│                 │                                                       │
└─────────────────┴───────────────────────────────────────────────────────┘
```

## Dashboard Page

```
┌─────────────────────────────────────────────────────────────────────┐
│  📊 Trading Dashboard                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Account Information                                                │
│  ┌───────────────┬───────────────┬───────────────┐                 │
│  │   Balance     │ Open Positions│  Daily P&L    │                 │
│  │  $10,000.00   │       3       │   +$125.50 ▲  │                 │
│  └───────────────┴───────────────┴───────────────┘                 │
│                                                                     │
│  ─────────────────────────────────────────────────────────────     │
│                                                                     │
│  Open Positions                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Symbol  │ Side │ Size │ Entry  │ Current │    P&L        │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ EUR/USD │ LONG │ 1.5  │ 1.0850 │ 1.0875  │ +$37.50 🟢   │   │
│  │ GBP/USD │ LONG │ 1.0  │ 1.2650 │ 1.2680  │ +$30.00 🟢   │   │
│  │ USD/JPY │ SHORT│ 2.0  │ 150.25 │ 150.05  │ +$40.00 🟢   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ─────────────────────────────────────────────────────────────     │
│                                                                     │
│  Recent Trades                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Time     │ Symbol  │Side │Size│Entry │Exit  │   P&L      │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ 14:23:15 │ EUR/USD │LONG │1.0 │1.0820│1.0850│ +$30.00 🟢 │   │
│  │ 13:45:32 │ GBP/USD │LONG │1.5 │1.2600│1.2625│ +$37.50 🟢 │   │
│  │ 12:18:44 │ USD/JPY │SHORT│2.0 │149.80│149.60│ +$40.00 🟢 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ℹ Dashboard updates automatically every 5 seconds                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Configuration Page

```
┌─────────────────────────────────────────────────────────────────────┐
│  ⚙️ Bot Configuration                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Trading Parameters                                                 │
│                                                                     │
│  Trading Pairs (comma-separated)                                    │
│  [EUR/USD,GBP/USD,USD/JPY                                      ]   │
│                                                                     │
│  ┌─────────────────────────┬─────────────────────────┐             │
│  │ Short MA Period         │ Risk per Trade (%)      │             │
│  │ [50              ]      │ [1.0            ]       │             │
│  │                         │                         │             │
│  │ Long MA Period          │ Stop Loss (%)           │             │
│  │ [200             ]      │ [1.0            ]       │             │
│  │                         │                         │             │
│  │ Timeframe               │ Take Profit (%)         │             │
│  │ [1h ▼            ]      │ [2.0            ]       │             │
│  └─────────────────────────┴─────────────────────────┘             │
│                                                                     │
│  Max Drawdown (%)                                                   │
│  [10.0                                                         ]   │
│                                                                     │
│  ─────────────────────────────────────────────────────────────     │
│                                                                     │
│  ┌─────────────┬─────────────┬─────────────┐                       │
│  │ 💾 Save     │ ▶️ Start    │ ⏹️ Stop     │                       │
│  │ Config      │ Bot         │ Bot         │                       │
│  └─────────────┴─────────────┴─────────────┘                       │
│                                                                     │
│  ℹ Configuration Tips:                                             │
│    • Start with conservative settings (low risk, tight stops)      │
│    • Test with OANDA practice account before going live            │
│    • Monitor the bot regularly and adjust as needed                │
│    • Use stop losses on every trade                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## AI Assistant Page

```
┌─────────────────────────────────────────────────────────────────────┐
│  🤖 AI Trading Assistant                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ℹ Ask questions about your portfolio, trading strategy, or get    │
│    market insights.                                                 │
│                                                                     │
│  Quick Queries                                                      │
│  ┌───────────────┬───────────────┬───────────────┐                 │
│  │ 📊 Analyze    │ ⚠️ Risk       │ 💡 Get        │                 │
│  │   Portfolio   │   Assessment  │   Suggestions │                 │
│  └───────────────┴───────────────┴───────────────┘                 │
│                                                                     │
│  ─────────────────────────────────────────────────────────────     │
│                                                                     │
│  Chat History                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  You: Analyze my current portfolio                         │   │
│  │                                                             │   │
│  │  AI: Based on your current positions, you have a well-     │   │
│  │      diversified portfolio across three major currency     │   │
│  │      pairs. Your risk exposure is moderate with...         │   │
│  │                                                             │   │
│  │  You: What about the risk level?                           │   │
│  │                                                             │   │
│  │  AI: Your current risk level is within acceptable          │   │
│  │      parameters. With 1% risk per trade and...             │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ─────────────────────────────────────────────────────────────     │
│                                                                     │
│  Your question: [                                    ]  [Send]     │
│                                                                     │
│  [🗑️ Clear Chat History]                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Logs Page

```
┌─────────────────────────────────────────────────────────────────────┐
│  📋 System Logs                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Log Output                                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ [2024-10-03 14:23:15] Bot started                          │   │
│  │ [2024-10-03 14:23:16] Bot components initialized           │   │
│  │ [2024-10-03 14:23:20] Fetching data for EUR/USD            │   │
│  │ [2024-10-03 14:23:21] Signal: BUY for EUR/USD              │   │
│  │ [2024-10-03 14:23:22] Order placed: EUR/USD LONG 1.5       │   │
│  │ [2024-10-03 14:25:30] Fetching data for GBP/USD            │   │
│  │ [2024-10-03 14:25:31] Signal: BUY for GBP/USD              │   │
│  │ [2024-10-03 14:25:32] Order placed: GBP/USD LONG 1.0       │   │
│  │ [2024-10-03 14:28:15] Position monitoring: EUR/USD +$25    │   │
│  │ [2024-10-03 14:30:00] Daily P&L update: +$125.50           │   │
│  │ [2024-10-03 14:32:10] AI query: Analyze portfolio          │   │
│  │ [2024-10-03 14:35:00] Configuration saved                  │   │
│  │                                                             │   │
│  │                                                             │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  [🗑️ Clear Logs]    [💾 Export Logs]                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Visual Features

### Color Coding
- **Green (🟢)**: Positive P&L, successful operations
- **Red (🔴)**: Negative P&L, stopped status
- **Blue (ℹ️)**: Information messages
- **Yellow (⚠️)**: Warnings

### Status Indicators
- **Bot Status**: 🟢 Running / 🔴 Stopped
- **Profit**: ▲ Up arrow for gains
- **Loss**: ▼ Down arrow for losses

### Interactive Elements
- Buttons: Rounded with icons
- Input fields: Clean white backgrounds
- Tables: Striped rows for readability
- Metrics: Large, bold numbers

### Responsive Design
- Adapts to different screen sizes
- Mobile-friendly layout
- Touch-friendly controls

## Comparison with Tkinter GUI

| Feature | Tkinter | Streamlit |
|---------|---------|-----------|
| Interface Type | Desktop | Web Browser |
| Visual Design | Basic | Modern |
| Real-time Updates | Manual refresh | Auto-refresh |
| Accessibility | Local only | Network accessible |
| Mobile Support | No | Yes |
| Installation | Requires Tkinter | Just Python |
| Maintenance | Complex | Simple |
| Extensibility | Limited | Excellent |
