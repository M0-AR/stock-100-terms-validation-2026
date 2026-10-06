"""EXP03 — Buy-the-dip vs buy-and-hold + compounding (video Parts 5-6).
Dip rule: if daily close is >5% below trailing 20d high, invest next-day; else hold cash at rf.
Buy-hold: fully invested. Same capital, same window. Reports terminal wealth ratio + trades.
"""
import pandas as pd
from src.config import RISK_FREE_ANNUAL, BUY_DIP_THRESHOLD

def buy_dip_vs_hold(prices: pd.Series):
    px = prices.dropna()
    rets = px.pct_change().fillna(0)
    peak = px.rolling(20).max()
    dip = (px / peak - 1) < BUY_DIP_THRESHOLD
    rf_daily = (1 + RISK_FREE_ANNUAL) ** (1 / 252) - 1
    # buy-hold wealth
    bh = (1 + rets).cumprod()
    # dip-timer: invested only day after dip signal, else cash
    invested = dip.shift(1).fillna(False)
    strat_rets = rets.where(invested, rf_daily)
    dip_w = (1 + strat_rets).cumprod()
    exposure = float(invested.mean() * 100)
    return {"buy_hold_terminal": round(float(bh.iloc[-1]), 3),
            "dip_timer_terminal": round(float(dip_w.iloc[-1]), 3),
            "dip_timer_vs_hold_pct": round(float(dip_w.iloc[-1] / bh.iloc[-1] - 1) * 100, 2),
            "time_in_market_pct": round(exposure, 1),
            "n_dip_days": int(dip.sum()),
            "note": "negative gap = dip-timing underperforms buy-hold (cash-drag + whipsaw)"}
