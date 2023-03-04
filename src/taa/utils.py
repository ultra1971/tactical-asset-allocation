"""Utility functions such as volatility estimators and statistical measures."""
import numpy as np
import pandas as pd


def calculate_rolling_volatility(
    returns: pd.DataFrame,
    lookback: int = 21,
    factor: int = 252,
    estimator: str = "hist",
    decay: float = 0.97,
) -> pd.DataFrame:
    """Calculate historical volatility for all calendar days.

    Currently supported estimators are ``hist`` (realised standard deviation over lookback) and
    ``ewm`` (exponentially weighted with decay factor equal to :math:`1 - \lambda`).

    Args:
        returns (pd.DataFrame): table of asset returns
        lookback (int, optional): window over which vol is calculated. Defaults to 21.
        factor (int, optional): number of business days in a year. Defaults to 252.
        decay (float, optional): half life, or lambda, if using EWMA. Defaults to 0.97.
        estimator (str, optional): volatility estimator. Defaults to hist.

    Returns:
        pd.DataFrame: time series of volatilities matching rebalance dates

    Raises:
        NotImplementedError: when estimator is invalid
    """
    if estimator == "hist":
        rolling_volatility = returns.rolling(lookback).std()
    elif estimator == "ewm":
        rolling_volatility = returns.ewm(alpha=1 - decay).std()
    else:
        raise NotImplementedError
    return rolling_volatility.asfreq("D").ffill() * np.sqrt(factor)
