"""EXP04 — Diversification / asset allocation / rebalancing / beta-alpha-Sharpe-correlation
(video Part 8). Compares: 100% SPY vs 60/40 (SPY/GLD proxy for bonds/cash-like) vs
multi-asset basket; annual rebalance; reports beta/alpha vs SPY, correlation matrix.
"""
import pandas as pd
from src.metrics import daily_returns, cagr, ann_vol, sharpe, max_drawdown, beta_alpha, correlation
from src.config import RISK_FREE_ANNUAL, BENCHMARK

def diversification(prices):
    px = prices.dropna()
    bench_rets = daily_returns(px[BENCHMARK])
    res = {}
    ports = {
        "100pct_SPY": {"SPY": 1.0},
        "60_40_SPY_GLD": {"SPY": 0.6, "GLD": 0.4},
        "4ASSET_EQW": {"SPY": 0.25, "AAPL": 0.25, "KO": 0.25, "GLD": 0.25},
    }
    avail = {k: {a: w for a, w in v.items() if a in px.columns} for k, v in ports.items()}
    for name, w in avail.items():
        tot = sum(w.values())
        w = {a: x / tot for a, x in w.items()}
        port_rets = sum(daily_returns(px[a]) * wt for a, wt in w.items())
        port_px = (1 + port_rets).cumprod()
        b, a_ = beta_alpha(port_rets, bench_rets)
        res[name] = {"CAGR_pct": round(cagr(port_px) * 100, 2),
                     "vol_pct": round(ann_vol(port_rets) * 100, 2),
                     "sharpe": round(sharpe(port_rets, RISK_FREE_ANNUAL), 2),
                     "maxDD_pct": round(max_drawdown(port_px) * 100, 2),
                     "beta_vs_SPY": round(b, 2), "alpha_ann_pct": round(a_ * 100, 2)}
    # correlations: SPY vs each (systematic vs idiosyncratic illustration)
    corrs = {}
    for t in px.columns:
        if t != BENCHMARK:
            corrs[f"{BENCHMARK}_{t}"] = round(correlation(daily_returns(px[BENCHMARK]), daily_returns(px[t])), 2)
    res["correlations"] = corrs
    return res
