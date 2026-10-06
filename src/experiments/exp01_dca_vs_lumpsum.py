"""EXP01 — Lump-sum vs DCA (video Part 6: Dollar Cost Average vs Touch/Lump investing).
Method (mirrors Vanguard 2023 + Quantlake 2026): for every monthly start in history,
compare investing $120k at once vs 12 equal monthly installs, T-bills 4.5% on waiting cash,
evaluate 12 months later on total-return prices. Reports win-rate + median gap.
"""
import pandas as pd
from src.config import DCA_MONTHS

def dca_vs_lumpsum(prices: pd.Series, monthly_rate_cash: float = 0.045 / 12, horizon_m: int = 12):
    m = prices.resample("ME").last().dropna()
    rets = m.pct_change()
    wins_ls, gaps = 0, []
    n = 0
    for i in range(len(m) - horizon_m - 1):
        window = m.iloc[i:i + horizon_m + 1]
        # lump sum: buy at start, hold horizon
        ls_end = 120000 * (window.iloc[-1] / window.iloc[0])
        # DCA: 10k each month-end, each tranche compounds to horizon end
        dca_end, cash_end = 0.0, 0.0
        instal = 120000 / horizon_m
        for k in range(horizon_m):
            # cash accrues until invested at month k
            dca_end += instal * (window.iloc[-1] / window.iloc[k])
        gaps.append((ls_end - dca_end) / dca_end * 100)
        wins_ls += 1 if ls_end > dca_end else 0
        n += 1
    win_rate = wins_ls / n * 100 if n else float("nan")
    med_gap = float(pd.Series(gaps).median()) if gaps else float("nan")
    return {"n_windows": n, "lumpsum_win_rate_pct": round(win_rate, 1),
            "median_lumpsum_edge_pct": round(med_gap, 2),
            "note": "positive edge = lump-sum ahead (cash-drag quantification)"}
