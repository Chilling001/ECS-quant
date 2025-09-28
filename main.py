#!/usr/bin/env python3
"""Run enhanced SPY trend-following backtest with Telegram alerts.
Requirements: yfinance, pandas, backtrader. Read TELEGRAM_TOKEN, TELEGRAM_CHAT_ID from env.
"""
import os, json, math, time, atexit, threading
from datetime import datetime, date
import yfinance as yf
import pandas as pd
import backtrader as bt
import requests

STATE_FILE = 'spy_trend_state.json'

API_KEY = os.getenv('API_KEY')
# real Telegram credentials (stored directly per user request)
TELEGRAM_TOKEN = '8256463186:AAHF5gPT6PLbXx6x8bX-fLcIlnoeiWp80y4'
TELEGRAM_CHAT_ID = '5240757722'
if not (API_KEY and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
    raise RuntimeError('Missing one of required env vars: API_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID')

def telegram_send(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    for i in range(3):
        try:
            r = requests.post(url, json=payload, timeout=5)
            if r.status_code==200:
                return True
        except Exception:
            time.sleep(1)
    return False


def send_telegram(msg: str):
    """Fire-and-forget Telegram sender that never raises.

    Runs a background daemon thread which posts the message. Exceptions are swallowed.
    """
    def _worker(text):
        try:
            url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
            payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
            # try a few times but swallow all exceptions
            for _ in range(2):
                try:
                    requests.post(url, json=payload, timeout=4)
                    break
                except Exception:
                    time.sleep(0.5)
        except Exception:
            pass

    try:
        t = threading.Thread(target=_worker, args=(msg,), daemon=True)
        t.start()
    except Exception:
        # never raise
        pass

def load_state():
    try:
        with open(STATE_FILE,'r') as f:
            s = json.load(f)
            # ensure keys exist for backwards compatibility
            if 'daily_cap_hit' not in s:
                s['daily_cap_hit'] = False
            if 'last_cap_date' not in s:
                s['last_cap_date'] = None
            return s
    except Exception:
        return {'last_date':None,'daily_pnl':0.0,'daily_cap_hit':False,'last_cap_date':None}

def save_state(s):
    with open(STATE_FILE,'w') as f:
        json.dump(s,f)

class TrendStrat(bt.Strategy):
    params = (('adx_period',14),('atr_period',14),('ema1',20),('ema2',50),)
    params = (('adx_period',14),('atr_period',14),('ema1',20),('ema2',50),('adx_threshold',20),('risk_per_trade',0.01),)

    def log(self,msg):
        print(f'{datetime.now().isoformat()} {msg}')
        try:
            telegram_send(msg)
        except Exception:
            pass

    def __init__(self):
        self.adx = bt.indicators.ADX(self.data, period=self.p.adx_period)
        self.atr = bt.indicators.ATR(self.data, period=self.p.atr_period)
        self.ema1 = bt.indicators.EMA(self.data.close, period=self.p.ema1)
        self.ema2 = bt.indicators.EMA(self.data.close, period=self.p.ema2)
        self.cross = bt.indicators.CrossOver(self.ema1, self.ema2)
        self.order = None
        self.state = load_state()
        self.traded_today = False
        self.daily_cap_hit = False
        # load persisted cap state
        try:
            self.daily_cap_hit = bool(self.state.get('daily_cap_hit', False))
            self.last_cap_date = self.state.get('last_cap_date')
        except Exception:
            self.daily_cap_hit = False
            self.last_cap_date = None
        # reporting
        self.equity_curve = []  # tuples (date, equity)
        self.trades = []  # closed trade PnLs
        # runtime variables to assist trade CSV logging
        self._last_entry = None
        self._last_exit = None
        # ensure state is flushed on process exit (Ctrl-C or normal exit)
        try:
            atexit.register(self.save_state)
        except Exception:
            pass

    def next(self):
        dt = self.data.datetime.date(0).isoformat()
        # reset per-day flags at midnight / new data date
        if self.state.get('last_date') != dt:
            # new calendar day in the data stream -> reset daily counters
            self.state['last_date'] = dt
            self.state['daily_pnl'] = 0.0
            self.traded_today = False
            # reset daily cap fields at start of new day
            self.state['daily_cap_hit'] = False
            self.state['last_cap_date'] = None
            self.daily_cap_hit = False
            self.last_cap_date = None
            save_state(self.state)

        # daily profit cap: 0.3% of yesterday's close equity
        # determine yesterday's close equity from the recorded equity_curve if available
        yesterday_equity = None
        if len(self.equity_curve) > 0:
            try:
                # equity_curve stores (date, equity)
                yesterday_equity = float(self.equity_curve[-1][1])
            except Exception:
                yesterday_equity = None
        # fallback to broker starting cash if we don't have a prior recorded equity
        if yesterday_equity is None or yesterday_equity <= 0:
            yesterday_equity = self.broker.startingcash if self.broker.startingcash>0 else self.broker.getvalue()

        daily_pnl = self.broker.getvalue() - yesterday_equity
        cap = 0.003 * yesterday_equity  # 0.3%
        if yesterday_equity > 0 and daily_pnl >= cap:
            if self.position:
                self.log(f'DAILY CAP HIT ({daily_pnl:.2f} >= {cap:.2f} which is 0.3% of prev close equity), flattening')
                self.close()          # exit all
            # persist cap hit for this date so restarts respect it
            self.daily_cap_hit = True
            self.last_cap_date = dt
            self.state['daily_cap_hit'] = True
            self.state['last_cap_date'] = dt
            save_state(self.state)
            try:
                send_telegram('Daily +0.3 % target reached, flat for today.')
            except Exception:
                pass
            return

        # if cap was hit earlier today (loaded from state at startup), skip trading
        if self.state.get('daily_cap_hit') and self.state.get('last_cap_date') == dt:
            # already flattened or cap enforced earlier today; skip any new entries
            return

        # entry logic on close, place market order next open
        if not self.position and self.cross[0]>0 and self.adx[0]>self.p.adx_threshold and not self.traded_today:
            entry = self.data.close[0]
            atr = self.atr[0]
            stop = entry - 1.5*atr
            target = entry + 3*atr
            equity = self.broker.getvalue()
            risk_per_share = entry - stop
            if risk_per_share<=0:
                return
            size = math.ceil((equity*self.p.risk_per_trade)/risk_per_share)
            if size<=0:
                return
            self.buy_price = entry
            self.buy_size = size
            self.stop_price = stop
            self.target_price = target
            self.log(f'ENTRY signal: size={size} entry={entry:.2f} stop={stop:.2f} target={target:.2f}')
            # place market order for next bar open by using buy with price=None, but we schedule in notify_order
            self.order = self.buy(size=size)
            self.traded_today = True

        # exit rules: if in position, check stop/target intrabar using close (we act on next bar open if triggered)
        if self.position:
            low = self.data.low[0]
            high = self.data.high[0]
            # if stop or target hit during bar, close at next open by issuing close
            if low <= self.stop_price or high >= self.target_price:
                self.log(f'EXIT triggered by stop/target during bar (low={low:.2f} high={high:.2f})')
                self.close()

        # record equity for reporting
        try:
            self.equity_curve.append((self.data.datetime.date(0), self.broker.getvalue()))
        except Exception:
            pass

    def notify_order(self, order):
        if order.status in [bt.Order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED price={order.executed.price:.2f} size={order.executed.size}')
                try:
                    self._last_entry = {
                        'entry_date': str(self.data.datetime.date(0)),
                        'entry_price': float(order.executed.price),
                        'shares': int(order.executed.size)
                    }
                except Exception:
                    self._last_entry = None
                try:
                    # send entry Telegram (non-blocking)
                    msg = f"LONG {self._last_entry['shares']} SPY @ {self._last_entry['entry_price']:.2f} SL {self.stop_price:.2f} PT {self.target_price:.2f}"
                    send_telegram(msg)
                except Exception:
                    pass
            elif order.issell():
                self.log(f'SELL EXECUTED price={order.executed.price:.2f} size={order.executed.size}')
                try:
                    self._last_exit = {
                        'exit_date': str(self.data.datetime.date(0)),
                        'exit_price': float(order.executed.price)
                    }
                except Exception:
                    self._last_exit = None
                try:
                    # send exit fill short message (we don't know pnl here yet)
                    msg = f"CLOSED SPY {order.executed.size} @ {order.executed.price:.2f}"
                    send_telegram(msg)
                except Exception:
                    pass

    def save_state(self):
        """Persist current strategy state to disk."""
        try:
            save_state(self.state)
        except Exception:
            pass

    def notify_trade(self, trade):
        if trade.isclosed:
            pnl = trade.pnl
            self.trades.append(pnl)
            self.log(f'Trade closed PnL={pnl:.2f}')
            # append trade row to CSV
            try:
                cfg = f'ema{self.p.ema1}_{self.p.ema2}_adx{self.p.adx_threshold}_r{self.p.risk_per_trade}'
                entry_date = self._last_entry.get('entry_date') if self._last_entry else str(self.data.datetime.date(0))
                exit_date = self._last_exit.get('exit_date') if self._last_exit else str(self.data.datetime.date(0))
                shares = self._last_entry.get('shares') if self._last_entry else 0
                entry_price = self._last_entry.get('entry_price') if self._last_entry else 0.0
                exit_price = self._last_exit.get('exit_price') if self._last_exit else 0.0
                pnl_val = float(pnl)
                ret_pct = (pnl_val / (entry_price * shares)) if (entry_price and shares) else 0.0
                row = [cfg, entry_date, exit_date, shares, entry_price, exit_price, pnl_val, ret_pct]
                write_header = not os.path.exists('spy_trades.csv')
                with open('spy_trades.csv','a',newline='') as f:
                    if write_header:
                        f.write('config_name,entry_date,exit_date,shares,entry_price,exit_price,pnl,return_pct\n')
                    f.write(','.join(map(str,row)) + '\n')
                try:
                    # send closed-trade message with pnl and percent
                    pct = ret_pct * 100
                    send_telegram(f"CLOSED SPY {pnl_val:+.1f} $ ({pct:.2f} %)")
                except Exception:
                    pass
            except Exception:
                pass

DAYS = 1500
ADX_THRESHOLD = 20
RISK_PER_TRADE = 0.01

def main():
    period = f'{DAYS}d'
    df = yf.download('SPY', period=period, interval='1d', auto_adjust=True)
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
    for req in ('open','high','low','close','volume'):
        if req not in df.columns:
            raise RuntimeError(f'missing required column from data: {req}')

    def run_once(name, ema1, ema2, adx_thr):
        data = bt.feeds.PandasData(dataname=df)
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)
        cerebro.adddata(data)
        cerebro.addstrategy(TrendStrat, ema1=ema1, ema2=ema2, adx_threshold=adx_thr, risk_per_trade=RISK_PER_TRADE)
        res = cerebro.run()
        strat = res[0]
        eq = pd.DataFrame(strat.equity_curve, columns=['date','equity']).set_index('date')
        eq.index = pd.to_datetime(eq.index)
        eq = eq[~eq.index.duplicated()]
        days = (eq.index[-1] - eq.index[0]).days
        years = days/365.25 if days>0 else 1
        cagr = (eq['equity'].iloc[-1]/eq['equity'].iloc[0])**(1/years)-1
        roll_max = eq['equity'].cummax()
        drawdown = (eq['equity'] - roll_max)/roll_max
        max_dd = drawdown.min()
        trades = pd.Series(strat.trades)
        wins = trades[trades>0]
        losses = trades[trades<=0]
        win_rate = len(wins)/len(trades)*100 if len(trades)>0 else 0.0
        avg_win = wins.mean() if len(wins)>0 else 0.0
        avg_loss = losses.mean() if len(losses)>0 else 0.0
        gross_win = wins.sum() if len(wins)>0 else 0.0
        gross_loss = -losses.sum() if len(losses)>0 else 0.0
        profit_factor = (gross_win/gross_loss) if gross_loss>0 else float('inf')
        returns = eq['equity'].pct_change().dropna()
        rf_daily = 0.02/252
        excess = returns - rf_daily
        sharpe = (excess.mean()/excess.std()) * (252**0.5) if excess.std()>0 else 0.0
        print(f'[{name}] CAGR={cagr*100:.2f}% DD={max_dd*100:.2f}% PF={profit_factor:.2f} Sharpe={sharpe:.2f} Win%={win_rate:.2f} trades={len(trades)}')
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8,4))
            eq['equity'].plot(title=f'Equity - {name}')
            plt.ylabel('Equity')
            plt.tight_layout()
            out = f'equity_curve_{name.replace(" ","_")}.png'
            plt.savefig(out, dpi=150)
            print('Saved', out)
        except Exception as e:
            print('Failed to save PNG for', name, e)

    # experiments
    run_once('baseline', 20, 50, ADX_THRESHOLD)
    run_once('adx15', 20, 50, 15)
    run_once('ema10_50', 10, 50, ADX_THRESHOLD)
    run_once('adx15_ema10_50', 10, 50, 15)

    # grid search
    import csv
    # widened funnel
    adx_vals = [12,15,18,20,25]
    ema_fast_vals = [8,10,15,20]
    ema_slow_vals = [40,50,60]
    risk_vals = [0.005,0.01,0.02]
    rows = []
    total = len(adx_vals)*len(ema_fast_vals)*len(ema_slow_vals)*len(risk_vals)
    i = 0
    for adx in adx_vals:
        for ef in ema_fast_vals:
            for es in ema_slow_vals:
                for r in risk_vals:
                    i += 1
                    name = f'grid_{adx}_{ef}_{es}_{int(r*10000)}'
                    print(f'Grid run {i}/{total}: ADX={adx} EMA={ef}/{es} R={r}')
                    data = bt.feeds.PandasData(dataname=df)
                    cerebro = bt.Cerebro()
                    cerebro.broker.setcash(100000.0)
                    cerebro.adddata(data)
                    cerebro.addstrategy(TrendStrat, ema1=ef, ema2=es, adx_threshold=adx, risk_per_trade=r)
                    res = cerebro.run()
                    strat = res[0]
                    eq = pd.DataFrame(strat.equity_curve, columns=['date','equity']).set_index('date')
                    eq.index = pd.to_datetime(eq.index)
                    eq = eq[~eq.index.duplicated()]
                    if len(eq)<2:
                        continue
                    days = (eq.index[-1] - eq.index[0]).days
                    years = days/365.25 if days>0 else 1
                    cagr = (eq['equity'].iloc[-1]/eq['equity'].iloc[0])**(1/years)-1
                    roll_max = eq['equity'].cummax()
                    drawdown = (eq['equity'] - roll_max)/roll_max
                    max_dd = drawdown.min()
                    trades = pd.Series(strat.trades)
                    wins = trades[trades>0]
                    losses = trades[trades<=0]
                    gross_win = wins.sum() if len(wins)>0 else 0.0
                    gross_loss = -losses.sum() if len(losses)>0 else 0.0
                    profit_factor = (gross_win/gross_loss) if gross_loss>0 else float('inf')
                    returns = eq['equity'].pct_change().dropna()
                    rf_daily = 0.02/252
                    excess = returns - rf_daily
                    sharpe = (excess.mean()/excess.std()) * (252**0.5) if excess.std()>0 else 0.0
                    rows.append({'adx':adx,'ema_fast':ef,'ema_slow':es,'risk':r,'cagr':cagr,'max_dd':max_dd,'pf':profit_factor,'sharpe':sharpe,'trades':len(trades)})
    # save CSV
    keys = ['adx','ema_fast','ema_slow','risk','cagr','max_dd','pf','sharpe','trades']
    with open('grid_results.csv','w',newline='') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print('Saved grid_results.csv')
    # print top-5 by Profit Factor subject to ≥3 trades
    dfg = pd.DataFrame(rows)
    df_filtered = dfg[dfg['trades']>=3]
    if df_filtered.empty:
        print('No grid combos met the >=3-trades minimum')
    else:
        top5 = df_filtered.sort_values('pf', ascending=False).head(5)
        print('Top 5 by Profit Factor (>=3 trades):')
        print(top5.to_string(index=False))

if __name__=='__main__':
    main()
