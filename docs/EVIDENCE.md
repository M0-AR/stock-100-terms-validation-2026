# Evidence log — every number in README traces to a verified fetch, not hand-edits

Date: 2026-10-06 UTC. Region: global/US market. All web searches sequential (one-at-a-time, 5s backoff on 429).

## 1. Literature (sequential searches, distinct keywords)
- `websearch` (deep): "dollar cost averaging vs lump sum investing empirical evidence 2026 Vanguard study" → Vanguard 2023 "Cost averaging: Invest now or temporarily hold your cash?" (LS wins ~68% of 1y windows, 1976–2022, edge 1.2–2.4pp; CA rational only under high loss-aversion). Quantlake 2026-09-28 (90 ETFs: LS ahead 69% vs 12-mo spread, median cost of spreading 3.2% of 5y wealth, first-year dip 5.6%→2.7%). Masterworks 2026-07-16, CompoundFig 2026-02-10, Money&Planet 2026-05/06 (hybrid 50–70% immediate + 6-mo DCA captures ~80% of LS edge, halves drawdown exposure).
- `duckduckgo_search`: "passive index ETF beat active stock picking SPIVA 2025 2026" → SPIVA H1-2026: 67% of large-cap active underperformed S&P 500 (10% index gain); 2025: 79% missed; 20y to Jun-2026: 92.6% of US large-cap active trailed, only ~51/690 survived+beat; 5y persistence ≈ chance.
- `webfetch lite.duckduckgo` fallback (openresearch web_search timed out twice): "buy the dip strategy backtest SP500 returns" → AlphaStrategicGrowth 36y drawdown study; InvestingPaths (dip-timing lost to index on 7 stocks + SP500/Nasdaq); BogleInvestor/Substack dip-buying system; Setup4Alpha SPY candlestick RealTest 2000–2026.
- `paper-search arxiv`: "dollar cost averaging lump sum passive investing benchmark" → Brown 2112.09807 (GBM lower bound, P(negative)<2.5% after 40y annual DCA); Sato 2601.06074 (effective-exposure framework: horizon ≠ risk reduction per unit exposure; DCA vs LS differ in exposure profile, constant-order gap).
- `paper-search unified` (semantic/openalex/crossref): "passive index funds outperform active management diversification Sharpe" → Heikkinen 2025 (active ESG: higher VaR/drawdown, no compensating return; closet-indexing); Cremers et al. JFE 2016 (indexing vs active, 360 cites); Fang & Parida JRFM 2025 (active sustainable did not beat passive in pre/crash/post-COVID).
- `agent-reach_search web`: "best practice backtesting stock strategy survivorship bias transaction costs 2026" → confirms adjustments: total-return (Adj Close), survivorship, fees/taxes, no lookahead.
- `kaggle`: search_everything "sp500 backtest dollar cost averaging" (0 hits), datasets_list/discussions_search (0/needs exact sort enum) — recorded as negative results, not hidden.
- `wiki_search`: "dollar cost averaging buy and hold index fund" → ETF / Investment strategy / Investment pages (DCA, DRIP definitions).
- `openresearch openalex`: "market timing underperformance retail investors Barber Odean" → Gempesaw et al. 2023 (retail ETF: chase prior returns, longer holds); Gorzon & von Nitzsch 2025 (behavioral attribution via OLS).
- `openresearch news`: "passive investing index funds outperform active 2026" → Sep/Oct-2026: note.com SPIVA Sep-2026 edition (80% pros lose), Moneycontrol small-cap active/passive cyclicality, Yahoo CA 2026-09-30 (only 13% beat index).
- `gsd_websearch` "reproducible finance research Docker backtest best practice 2026" → empty (recorded).
- `superpowers semantic_search_skills` → no finance skill; used generic research checklist only.
- `openresearch hacker_news` "dollar cost averaging lump sum backtest" → 0 hits (recorded).
- `paper-search semantic` "compound interest buy and hold long term equity premium" → [] (recorded).
- `gitmcp` ranaroussi/yfinance docs → `history(repair=True)`, `auto_adjust=True` for total-return, multi-level columns handling; adopted in `src/data.py`.

## 2. Live market verification (2026-10-06, no hand-edits)
- stock_quote (Yahoo/YFinance): AAPL 333.9201 (P/E 38.28, mcap 4.871T) · MSFT 535.00 (29.80, 3.973T) · NVDA 241.88 (30.58, 5.841T) · TSLA 381.375 (353.12, 1.506T) · KO 86.8501 (26.08, 0.374T) · SPY 779.44. Encoded in `src/config.py LIVE_SNAPSHOT`.
- SEC EDGAR (AAPL): rev 2025 $416.161B (+6.4% vs 2024 $391.035B), net $112.010B → margin 26.9%; assets $359.241B; equity $73.733B.
- CoinGecko BTC: $86,097.73 (2026-10-06); 30d range $75.6k–$86.4k (high-vol illustration).
- ECB/Frankfurter FX: USD→EUR 0.88739, USD→JPY 158.09 (EGP not in ECB basket — recorded gap for Egypt audience).
- yfinance per-ticker 5y histories (single-Ticker loop; batched download rate-limited): 2021-10-06→2026-10-06, 1,827 rows incl. BTC weekends, nan_rate 0.274 (weekend-mismatch, handled by inner-join in metrics). `src/results/prices.csv`.

## 3. Experiment outputs (run `python3 src/experiments/run_all.py`; full JSON in `src/results/results.json`)
- EXP01 DCA vs lump-sum on SPY: 48 rolling 12-mo windows; lump-sum win-rate **81.2%**, median edge **+6.6%** (direction matches Vanguard ~68% / Quantlake 69%; magnitude higher in this 5y bull window — reported as window-dependence, not contradiction).
- EXP02 passive vs active proxy: SPY CAGR **13.88%**, vol 17.73%, Sharpe 0.49, maxDD −24.5% · NVDA 63.66% / TSLA 7.85% / KO 13.38% / GLD 18.15% · 3/6 singles beat SPY; EQW basket +5.19pp gap — flagged as small-N survivorship-biased illustration, consistent with SPIVA long-run underperformance, not a refutation.
- EXP03 buy-dip (−5% vs 20d high) vs buy-hold: SPY dip-timer −21.78% terminal gap (13.4% time-in-market, 168 dip-days) · TSLA −64.74% (63.6% exposure, 798 dip-days).
- EXP04 diversification: 100% SPY Sharpe 0.59/maxDD −24.5% → 60/40 SPY/GLD Sharpe 0.86/maxDD −18.69% (beta 0.67, alpha +6.64pp) → 4-asset EQW Sharpe 0.94/maxDD −16.88%. Correlations: SPY–GLD 0.16, SPY–KO 0.26, SPY–BTC 0.41, SPY–AAPL/MSFT/NVDA 0.69–0.72.
- EXP05 live concentration: top-3 mcap share **88.7%** (NVDA 35.3/AAPL 29.4/MSFT 24.0); P/E spread 327.0 (TSLA 353.1 vs KO 26.1); AAPL net margin 26.9%.

All claims in README/PAPER map 1:1 to these artifacts. Nothing was hand-tuned after seeing results.
