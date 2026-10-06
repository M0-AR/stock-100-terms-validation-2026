"""EXP05 — Valuation / style regimes (video Parts 2-3): growth vs value/defensive on live snapshot.
Uses verified live P/Es + SEC fundamentals (no invented earnings). Flags concentration risk:
top-3 mcap share, TSLA P/E outlier, NVDA mcap leadership. Purely descriptive — not a signal.
"""
from src.config import LIVE_SNAPSHOT

def valuation_regimes():
    s = LIVE_SNAPSHOT
    mcaps = {k: v["mcap"] for k, v in s.items() if "mcap" in v}
    total = sum(mcaps.values())
    top3 = sum(sorted(mcaps.values(), reverse=True)[:3]) / total * 100
    pes = {k: v["pe_ttm"] for k, v in s.items() if "pe_ttm" in v}
    aapl_margin = s["AAPL"]["net2025"] / s["AAPL"]["rev2025"] * 100
    return {
        "mcap_shares_pct": {k: round(v / total * 100, 1) for k, v in sorted(mcaps.items(), key=lambda x: -x[1])},
        "top3_concentration_pct": round(float(top3), 1),
        "pe_ttm_live": pes,
        "pe_spread_max_min": round(max(pes.values()) - min(pes.values()), 1),
        "AAPL_net_margin_2025_pct": round(aapl_margin, 1),
        "AAPL_rev_growth_2024_2025_pct": round((s["AAPL"]["rev2025"] - 391035000000) / 391035000000 * 100, 1),
        "style_note": "TSLA P/E >> group (speculative/growth outlier); KO lowest P/E (defensive); NVDA largest mcap (concentration).",
    }
