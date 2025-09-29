#!/usr/bin/env python3
"""Asymmetric bot: 30% risk / 30% session-cap on 3x ETF SPXL.

Rules implemented:
- Start cash $100
- Instrument: SPXL (3x S&P 500)
- Entry: 20 EMA > 50 EMA and ADX(14) > 20
- Risk per trade: 30% of current equity
- Stop = entry - 1.5 ATR(14)
- No fixed profit target. Trailing stop = highest close since entry - 1 ATR
- Exit on EMA cross-down OR equity <= $70
- Session cap: realized+unrealized PnL >= +30% of session start equity -> flatten and lock for the session
- Persist session state in trendbot_state.json and trades in trendbot_trades.csv
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
            s = json.load(f)
            # ensure fields
            s.setdefault('session_start_equity', None)
            s.setdefault('session_locked', False)
            s.setdefault('session_trades', 0)
            s.setdefault('session_pnl', 0.0)
            s.setdefault('last_date', None)
            return s
    except Exception:
        return {'session_start_equity': None, 'session_locked': False, 'session_trades': 0, 'session_pnl': 0.0, 'last_date': None}


def save_state(s):
    with open(STATE_FILE, 'w') as f:
        json.dump(s, f)


class AsymmetricStrat(bt.Strategy):
    params = (
        ('adx_period', 14),
        ('atr_period', 14),
        ('ema1', 20),
        ('ema2', 50),
        ('adx_threshold', 20),
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
        self.entry_price = None
        self.stop_price = None
        self.highest_close = None
        self.state = load_state()
        # session fields
        self.session_start_equity = self.state.get('session_start_equity')
        self.session_locked = bool(self.state.get('session_locked', False))
        self.session_trades = int(self.state.get('session_trades', 0))
        self.session_pnl = float(self.state.get('session_pnl', 0.0))

    def next(self):
        dt = self.data.datetime.date(0).isoformat()
        # new session/day reset
        if self.state.get('last_date') != dt:
            self.state['last_date'] = dt
            # start session at current equity
            cur_equity = float(self.broker.getvalue())
            self.session_start_equity = cur_equity
            self.state['session_start_equity'] = cur_equity
            self.session_locked = False
            self.state['session_locked'] = False
            self.session_trades = 0
            self.state['session_trades'] = 0
            self.session_pnl = 0.0
            self.state['session_pnl'] = 0.0
            save_state(self.state)

        # if session locked, skip trading
        if self.state.get('session_locked'):
            return

        equity = float(self.broker.getvalue())

        # check hard floor
        if equity <= 70.0:
            # exit and lock session
            if self.position:
                self.log('Equity <= 70, exiting and locking session')
                self.close()
            self.session_locked = True
            self.state['session_locked'] = True
            save_state(self.state)
            # brag message
            try:
                pct = (equity - (self.session_start_equity or equity)) / (self.session_start_equity or equity) * 100 if self.session_start_equity else 0.0
                send_telegram(f"🎯 Session booked: {pct:+.2f}% in {self.session_trades} trades. Equity: ${self.session_start_equity:.2f} → ${equity:.2f}. Bot locked until next session.")
            except Exception:
                pass
            return

        # session cap check: realized + unrealized pnl >= 30% of session start equity
        if self.session_start_equity is not None:
            combined_pnl = equity - self.session_start_equity
            cap = 0.30 * self.session_start_equity
            if combined_pnl >= cap:
                # flatten and lock
                if self.position:
                    self.log('Session cap hit (+30%), flattening')
                    self.close()
                self.session_locked = True
                self.state['session_locked'] = True
                # update session pnl
                self.session_pnl = combined_pnl
                self.state['session_pnl'] = self.session_pnl
                save_state(self.state)
                try:
                    pct = (equity - self.session_start_equity) / self.session_start_equity * 100
                    send_telegram(f"🎯 Session booked: {pct:+.2f}% in {self.session_trades} trades. Equity: ${self.session_start_equity:.2f} → ${equity:.2f}. Bot locked until next session.")
                except Exception:
                    pass
                return

        # entry logic
        if not self.position and self.cross[0] > 0 and self.adx[0] > self.p.adx_threshold:
            entry = float(self.data.close[0])
            atr = float(self.atr[0])
            stop = entry - 1.5 * atr
            risk_per_trade = 0.30  # 30% of equity
            if stop >= entry:
                return
            size = math.floor((equity * risk_per_trade) / (entry - stop))
            if size <= 0:
                return
            self.entry_price = entry
            self.stop_price = stop
            self.highest_close = entry
            self.log(f'ENTRY: size={size} entry={entry:.2f} stop={stop:.2f} (risk 30% of ${equity:.2f})')
            self.buy(size=size)

        # manage open position
        if self.position:
            # update highest close
            self.highest_close = max(self.highest_close or 0.0, float(self.data.close[0]))
            trailing_stop = self.highest_close - float(self.atr[0]) if self.highest_close is not None else None
            low = float(self.data.low[0])
            # trailing stop hit
            if trailing_stop is not None and low <= trailing_stop:
                self.log('Trailing stop hit, closing position')
                self.close()
                return
            # ema cross-down exit
            if self.ema_fast[0] < self.ema_slow[0]:
                self.log('EMA cross-down exit')
                self.close()

    def notify_order(self, order):
        if order.status in [bt.Order.Completed]:
            if order.isbuy():
                price = float(order.executed.price)
                size = int(order.executed.size)
                self.log(f'BUY EXECUTED price={price:.2f} size={size}')
                try:
                    send_telegram(f'LONG {size} SPXL @ {price:.2f} SL {self.stop_price:.2f}')
                except Exception:
                    pass
            elif order.issell():
                price = float(order.executed.price)
                size = int(order.executed.size)
                self.log(f'SELL EXECUTED price={price:.2f} size={size}')
                try:
                    send_telegram(f'CLOSED SPXL @ {price:.2f}')
                except Exception:
                    pass

    def notify_trade(self, trade):
        if trade.isclosed:
            try:
                shares_val = getattr(trade, 'size', None)
                if shares_val is None:
                    shares_val = (None)
                shares = int(shares_val) if shares_val is not None else 0
                entry_price = float(self.entry_price) if self.entry_price is not None else 0.0
                exit_price = float(trade.price) if hasattr(trade, 'price') else 0.0
                pnl = float(trade.pnl)
                date_in = (self.state.get('last_date') or '')
                date_out = str(self.data.datetime.date(0))
                write_header = not os.path.exists(TRADES_FILE)
                with open(TRADES_FILE, 'a', newline='') as f:
                    if write_header:
                        f.write('date_in,date_out,shares,entry,exit,pnl\n')
                    f.write(f"{date_in},{date_out},{shares},{entry_price},{exit_price},{pnl}\n")
                # update session counters
                self.session_trades += 1
                self.session_pnl = float(self.broker.getvalue()) - float(self.session_start_equity or 0.0)
                self.state['session_trades'] = self.session_trades
                self.state['session_pnl'] = self.session_pnl
                save_state(self.state)
                try:
                    send_telegram(f'CLOSED SPXL {pnl:+.1f} $')
                except Exception:
                    pass
            except Exception:
                pass


def main():
    DAYS = 60
    df = yf.download('SPXL', period=f'{DAYS}d', interval='1d', auto_adjust=True)
    df.dropna(inplace=True)
    # normalize
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
    cerebro.broker.setcash(100.0)
    cerebro.adddata(data)
    cerebro.addstrategy(AsymmetricStrat)
    cerebro.run()


if __name__ == '__main__':
    main()
