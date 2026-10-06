"""Shared config — tickers map directly to the 9-part taxonomy in the video."""
TICKERS = ["SPY", "AAPL", "MSFT", "NVDA", "TSLA", "KO", "GLD", "BTC-USD"]
BENCHMARK = "SPY"
PERIOD = "5y"
INTERVAL = "1d"
RISK_FREE_ANNUAL = 0.045  # 2026 HYSA/T-bill context from Vanguard/Quantlake research
DCA_MONTHS = 12
BUY_DIP_THRESHOLD = -0.05  # -5% from trailing 20d high
SEED = 2026
RESULTS_DIR = "src/results"
# Live snapshot verified 2026-10-06 via stock_quote + SEC EDGAR + CoinGecko (see docs/EVIDENCE.md)
LIVE_SNAPSHOT = {
    "AAPL": {"price": 333.9201, "pe_ttm": 38.281006, "mcap": 4871688814592, "rev2025": 416161000000, "net2025": 112010000000},
    "MSFT": {"price": 535.0, "pe_ttm": 29.804455, "mcap": 3972592566272},
    "NVDA": {"price": 241.88, "pe_ttm": 30.579016, "mcap": 5840676323328},
    "TSLA": {"price": 381.375, "pe_ttm": 353.12036, "mcap": 1506238922752},
    "KO": {"price": 86.8501, "pe_ttm": 26.081112, "mcap": 373676802048},
    "SPY": {"price": 779.44},
    "BTC": {"price": 86097.73},
    "FX": {"USD_EUR": 0.88739, "USD_JPY": 158.09},
}
