"""Metrics with textbook definitions — no lookahead, total-return (Adj Close) basis."""
import numpy as np
import pandas as pd

TRADING_DAYS = 252

def daily_returns(prices: pd.Series) -> pd.Series:
    return prices.pct_change().dropna()

def cagr(prices: pd.Series) -> float:
    prices = prices.dropna()
    if len(prices) < 2:
        return float("nan")
    years = (prices.index[-1] - prices.index[0]).days / 365.25
    if years <= 0:
        return float("nan")
    return float((prices.iloc[-1] / prices.iloc[0]) ** (1 / years) - 1)

def ann_vol(rets: pd.Series) -> float:
    return float(rets.std() * np.sqrt(TRADING_DAYS)) if len(rets) > 1 else float("nan")

def sharpe(rets: pd.Series, rf_annual: float = 0.045) -> float:
    if len(rets) < 2:
        return float("nan")
    rf_daily = (1 + rf_annual) ** (1 / TRADING_DAYS) - 1
    excess = rets - rf_daily
    sd = excess.std()
    if sd == 0 or np.isnan(sd):
        return float("nan")
    return float(excess.mean() / sd * np.sqrt(TRADING_DAYS))

def max_drawdown(prices: pd.Series) -> float:
    roll_max = prices.cummax()
    dd = (prices - roll_max) / roll_max
    return float(dd.min())

def beta_alpha(asset_rets: pd.Series, bench_rets: pd.Series):
    df = pd.concat([asset_rets, bench_rets], axis=1, join="inner").dropna()
    if len(df) < 10:
        return float("nan"), float("nan")
    x = df.iloc[:, 1].values
    y = df.iloc[:, 0].values
    cov = np.cov(y, x)
    beta = float(cov[0, 1] / cov[1, 1]) if cov[1, 1] != 0 else float("nan")
    alpha_daily = float(y.mean() - beta * x.mean())
    alpha_ann = float((1 + alpha_daily) ** TRADING_DAYS - 1)
    return beta, alpha_ann

def correlation(a: pd.Series, b: pd.Series) -> float:
    df = pd.concat([a, b], axis=1, join="inner").dropna()
    if len(df) < 10:
        return float("nan")
    return float(df.iloc[:, 0].corr(df.iloc[:, 1]))
