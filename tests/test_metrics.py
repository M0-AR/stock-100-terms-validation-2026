import pandas as pd
from src.metrics import cagr, sharpe, max_drawdown, beta_alpha

def test_cagr_doubles_in_5y():
    import numpy as np
    idx = pd.date_range("2020-01-01", periods=5 * 252, freq="B")
    vals = 100 * (2 ** (np.arange(len(idx)) / len(idx)))
    px = pd.Series(vals, index=idx)
    g = cagr(px)
    assert 0.13 < g < 0.16, g

def test_max_dd():
    px = pd.Series([100, 120, 80, 100], index=pd.date_range("2024-01-01", periods=4))
    assert abs(max_drawdown(px) - (-1 / 3)) < 1e-9

def test_beta_self_is_one():
    import numpy as np
    idx = pd.date_range("2024-01-01", periods=100, freq="B")
    r = pd.Series(np.random.default_rng(0).normal(0, 0.01, 100), index=idx)
    b, a = beta_alpha(r, r)
    assert abs(b - 1.0) < 1e-9
    assert abs(a) < 1e-9
