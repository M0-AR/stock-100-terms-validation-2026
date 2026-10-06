"""Run all experiments end-to-end, write JSON + CSV into src/results/."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pandas as pd
from src.config import TICKERS, PERIOD, INTERVAL, SEED, RESULTS_DIR, BENCHMARK
from src.data import load_prices
from src.experiments.exp01_dca_vs_lumpsum import dca_vs_lumpsum
from src.experiments.exp02_passive_vs_active import passive_vs_active
from src.experiments.exp03_buy_dip import buy_dip_vs_hold
from src.experiments.exp04_diversification import diversification
from src.experiments.exp05_valuation import valuation_regimes

os.makedirs(RESULTS_DIR, exist_ok=True)
px, meta = load_prices(TICKERS, PERIOD, INTERVAL, SEED)
px.to_csv(os.path.join(RESULTS_DIR, "prices.csv"))
results = {"meta": {**meta, "tickers": list(px.columns), "rows": len(px),
                    "start": str(px.index[0].date()), "end": str(px.index[-1].date())}}
results["EXP01_DCA_vs_Lumpsum_SPY"] = dca_vs_lumpsum(px[BENCHMARK]) if BENCHMARK in px.columns else {}
results["EXP02_Passive_vs_Active"] = passive_vs_active(px)
results["EXP03_BuyDip_SPY"] = buy_dip_vs_hold(px[BENCHMARK]) if BENCHMARK in px.columns else {}
results["EXP03_BuyDip_TSLA"] = buy_dip_vs_hold(px["TSLA"]) if "TSLA" in px.columns else {}
results["EXP04_Diversification"] = diversification(px)
results["EXP05_Valuation_live"] = valuation_regimes()
with open(os.path.join(RESULTS_DIR, "results.json"), "w") as f:
    json.dump(results, f, indent=2)
print(json.dumps(results, indent=2))
print(f"\n[run_all] wrote {RESULTS_DIR}/results.json + prices.csv")
