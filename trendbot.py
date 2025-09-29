#!/usr/bin/env python3
"""Trendbot: EMA crossover + ADX strategy with ATR stops/targets.

60-day SPY feed, Backtrader strategy, Telegram alerts, CSV & state persistence.
"""
import os
import json
import math
import threading
from datetime import datetime
import yfinance as yf
import pandas as pd
import backtrader as bt

STATE_FILE = 'trendbot_state.json'
TRADES_FILE = 'trendbot_trades.csv'

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
if not (TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
    raise RuntimeError('Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in environment')


def send_telegram(msg: str):
    def _worker(text):
        try:
            import requests
            url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
            payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
            try:
                requests.post(url, json=payload, timeout=4)
            except Exception:
                pass
        except Exception:
            pass

    t = threading.Thread(target=_worker, args=(msg,), daemon=True)
    t.start()


def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {'last_trade': None, 'running_pnl': 0.0}


def save_state(s):
    with open(STATE_FILE, 'w') as f:
        json.dump(s, f)


class TrendStrat(bt.Strategy):
    params = (
        ('adx_period', 14),
        ('atr_period', 14),
        ('ema1', 20),
        ('ema2', 50),
        ('adx_threshold', 20),
        ('risk_per_trade', 0.005),  # 0.5% equity
    )

    def log(self, msg):
        print(f'{datetime.now().isoformat()} {msg}')

    def __init__(self):
        self.adx = bt.indicators.ADX(self.data, period=self.p.adx_period)
        self.atr = bt.indicators.ATR(self.data, period=self.p.atr_period)
        self.ema_fast = bt.indicators.EMA(self.data.close, period=self.p.ema1)
        self.ema_slow = bt.indicators.EMA(self.data.close, period=self.p.ema2)
        self.cross = bt.indicators.CrossOver(self.ema_fast, self.ema_slow)
        self.order = None
        self.stop_price = None
        self.target_price = None
        self.entry_info = None
        self.state = load_state()

    def next(self):
        # Entry: 20 EMA > 50 EMA and ADX(14) > 20
        if not self.position and self.cross[0] > 0 and self.adx[0] > self.p.adx_threshold:
            entry = float(self.data.close[0])
            atr = float(self.atr[0])
            stop = entry - 1.5 * atr
            target = entry + 3.0 * atr
            equity = float(self.broker.getvalue())
            risk_per_share = entry - stop
            if risk_per_share <= 0:
                return
            size = math.floor((equity * self.p.risk_per_trade) / risk_per_share)
            if size <= 0:
                return
            self.stop_price = stop
            self.target_price = target
            self.entry_info = {'entry_date': str(self.data.datetime.date(0)), 'shares': int(size), 'entry_price': entry}
            self.log(f'ENTRY signal: size={size} entry={entry:.2f} stop={stop:.2f} target={target:.2f}')
            self.order = self.buy(size=size)

        # Exit: if in position, check stop/target intrabar or ema cross down
        if self.position:
            low = float(self.data.low[0])
            high = float(self.data.high[0])
            # stop or target hit
            if (self.stop_price is not None and low <= self.stop_price) or (self.target_price is not None and high >= self.target_price):
                self.log(f'EXIT triggered by stop/target during bar (low={low:.2f} high={high:.2f})')
                self.close()
                return
            # ema fast crosses below slow -> exit
            if self.ema_fast[0] < self.ema_slow[0]:
                self.log('EXIT triggered by EMA crossover down')
                self.close()

    def notify_order(self, order):
        if order.status in [bt.Order.Completed]:
            if order.isbuy():
                price = float(order.executed.price)
                size = int(order.executed.size)
                self.log(f'BUY EXECUTED price={price:.2f} size={size}')
                # send entry Telegram (non-blocking)
                try:
                    send_telegram(f'LONG {size} SPY @ {price:.2f} SL {self.stop_price:.2f} PT {self.target_price:.2f}')
                except Exception:
                    pass
            elif order.issell():
                price = float(order.executed.price)
                size = int(order.executed.size)
                self.log(f'SELL EXECUTED price={price:.2f} size={size}')
                try:
                    send_telegram(f'CLOSED SPY @ {price:.2f}')
                except Exception:
                    pass

    def notify_trade(self, trade):
        if trade.isclosed:
            try:
                # shares: prefer trade.size, fallback to entry_info
                shares_val = getattr(trade, 'size', None)
                if shares_val is None:
                    shares_val = (self.entry_info.get('shares') if self.entry_info else None)
                shares = int(shares_val) if shares_val is not None else 0
                entry_price = float(self.entry_info.get('entry_price')) if self.entry_info else 0.0
                exit_price = float(trade.price) if hasattr(trade, 'price') else 0.0
                pnl = float(trade.pnl)
                date_in = (self.entry_info.get('entry_date') if self.entry_info else '')
                date_out = str(self.data.datetime.date(0))
                # append to CSV
                write_header = not os.path.exists(TRADES_FILE)
                with open(TRADES_FILE, 'a', newline='') as f:
                    if write_header:
                        f.write('date_in,date_out,shares,entry,exit,pnl\n')
                    f.write(f"{date_in},{date_out},{shares},{entry_price},{exit_price},{pnl}\n")
                # update state
                s = self.state
                s['last_trade'] = {'date_in': date_in, 'date_out': date_out, 'pnl': pnl}
                s['running_pnl'] = float(s.get('running_pnl', 0.0)) + pnl
                save_state(s)
                try:
                    send_telegram(f'CLOSED SPY {pnl:+.1f} $')
                except Exception:
                    pass
            except Exception:
                pass


def main():
    DAYS = 60
    df = yf.download('SPY', period=f'{DAYS}d', interval='1d', auto_adjust=True)
    df.dropna(inplace=True)
    # normalize columns
    new_cols = []
    for c in df.columns:
        if isinstance(c, tuple):
            new_cols.append(str(c[0]).lower())
        else:
            new_cols.append(str(c).lower())
    df.columns = new_cols
    if 'adj close' in df.columns and 'close' not in df.columns:
        df['close'] = df['adj close']
    for req in ('open', 'high', 'low', 'close', 'volume'):
        if req not in df.columns:
            raise RuntimeError(f'missing required column from data: {req}')

    data = bt.feeds.PandasData(dataname=df)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    cerebro.adddata(data)
    cerebro.addstrategy(TrendStrat)
    cerebro.run()


if __name__ == '__main__':
    main()
