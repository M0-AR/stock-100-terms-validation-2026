"""EXP02 — Passive (SPY buy-hold) vs naive stock-picking basket (video Parts 3-4).
Proxy for SPIVA claim: equal-weight basket of 5 single names vs SPY on same window.
Reports CAGR/vol/Sharpe/maxDD + hit-rate of single names beating SPY.
"""
from src.metrics import daily_returns, cagr, ann_vol, sharpe, max_drawdown
from src.config import RISK_FREE_ANNUAL

def passive_vs_active(prices, bench="SPY"):
    out = {}
    names = [c for c in prices.columns if c != bench and c != "BTC-USD"]
    for t in [bench] + names:
        r = daily_returns(prices[t])
        out[t] = {"CAGR_pct": round(cagr(prices[t]) * 100, 2),
                  "vol_pct": round(ann_vol(r) * 100, 2),
                  "sharpe": round(sharpe(r, RISK_FREE_ANNUAL), 2),
                  "maxDD_pct": round(max_drawdown(prices[t]) * 100, 2)}
    # equal-weight active basket (monthly rebalance approx via daily mean)
    basket_rets = sum(daily_returns(prices[t]) for t in names) / len(names)
    basket_px = (1 + basket_rets).cumprod()
    out["ACTIVE_EQW_BASKET"] = {"CAGR_pct": round(cagr(basket_px) * 100, 2),
                                "vol_pct": round(ann_vol(basket_rets) * 100, 2),
                                "sharpe": round(sharpe(basket_rets, RISK_FREE_ANNUAL), 2),
                                "maxDD_pct": round(max_drawdown(basket_px) * 100, 2)}
    bench_cagr = out[bench]["CAGR_pct"]
    beat = sum(1 for t in names if out[t]["CAGR_pct"] > bench_cagr)
    out["summary"] = {"singles_beating_SPY": f"{beat}/{len(names)}",
                      "basket_vs_SPY_CAGR_gap": round(out["ACTIVE_EQW_BASKET"]["CAGR_pct"] - bench_cagr, 2)}
    return out
