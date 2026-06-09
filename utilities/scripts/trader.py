#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "pytest",
#     "quantstats",
#     "scipy",
#     "typer",
#     "yfinance",
# ]
# ///

"""
Risk & CAPM (Capital Asset Pricing Model) analysis with yfinance
===========================================================
Implements the Yale 'Financial Markets' concepts:
  - Value at Risk (VaR)            : historical + parametric
  - Beta (regression slope)        : cov(asset, mkt) / var(mkt)
  - CAPM expected return           : R_f + beta*(E[R_m]-R_f)
  - Market vs idiosyncratic risk   : var(R) = beta^2*var(R_m) + var(epsilon)
"""

import datetime
import typer
import numpy as np
import pandas as pd
import pytest
import quantstats as qs  # For technical analysis (RSI, MACD, etc.) see `pandas-ta`
import yfinance as yf
from scipy import stats

# ----------------------------------------------------------------------
# Defaults
# ----------------------------------------------------------------------
ASSET = 'QCI.DE'  # Qualcomm on Xetra (Xetra = Exchange Electronic Trading; the primary venue for DAX-listed stocks)
MARKET = '^GDAXI'  # DAX index as the German market proxy.
LAST_YEAR = datetime.date.today().year - 1
SPAN = 5
BEGIN   = LAST_YEAR - SPAN
END     = LAST_YEAR
INTERVAL = '1d'  # yfinance intraday (e.g. '60m','15m','1m') only goes back a little; daily for multi-year.

# Annualisation factor (trading days). Use 252 for daily data.
PERIODS_PER_YEAR = 252

# Risk-free (annual) rate (expressed as a decimal).
# It is the return you would get by doing low risk investment e.g. in government bonds.
# It is the baseline to compare the asset against - investment should beat this rate,
# otherwise why take the risk?
RISK_FREE_ANNUAL = 0.03

# VaR settings
VAR_CONFIDENCE = 0.99  # 99% VaR
PORTFOLIO_VALUE = 1_000_000  # currency units, to express VaR in EUR


# ----------------------------------------------------------------------
# 1. Data
# ----------------------------------------------------------------------
def load_prices(tickers: list[str], begin: str, end: str, interval: str) -> pd.DataFrame:
    """Download Close prices, return a clean aligned DataFrame."""
    raw = yf.download(
        tickers, start=begin, end=end, interval=interval,
        auto_adjust=True, progress=False,
    )
    # With multiple tickers yfinance returns a column MultiIndex; grab Close.
    close = raw['Close'] if 'Close' in raw.columns.get_level_values(0) else raw
    close = close.dropna(how='all').ffill().dropna()
    return close


def prices_to_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Continuously compounded (log) returns: r = log(P_t / P_{t-1}).
    Assumes gains are reinvested instantaneously rather than at discrete
    intervals, equivalent to the rate r such that P_{t-1} * e^r = P_t.
    Used because multi-day returns are a simple sum of daily returns, which
    makes variance, regression, and VaR arithmetic straightforward."""
    return np.log(prices / prices.shift(1)).dropna()


# ----------------------------------------------------------------------
# 2. Value at Risk
# Two estimates are computed and printed side by side:
#   historical_var: no distributional assumption - the actual 1st percentile
#     of observed losses.
#   parametric_var: assumes normally distributed returns, fitting a Gaussian
#     from the mean and std of the return series.
# Example: 1-day 99% VaR = $1M means P(loss > $1M) = 1% per day.
# (where 99% is the confidence and returns prescribe distribution of losses)
# ----------------------------------------------------------------------
def historical_var(returns: pd.Series, confidence: float) -> float:
    """Historical (empirical) VaR as a positive loss fraction.
    VaR = the (1-confidence) quantile of the loss distribution."""
    losses = -returns
    return np.quantile(losses, confidence)


def parametric_var(returns: pd.Series, confidence: float) -> float:
    """Gaussian (variance-covariance) VaR as a positive loss fraction."""
    mu, sigma = returns.mean(), returns.std(ddof=1)
    # ppf (percent point function) is the inverse of the CDF (cumulative
    # distribution function). The CDF answers "given a value x, what fraction
    # of outcomes fall below x?"; ppf answers the reverse: "given a
    # probability p, what value x has exactly p of outcomes below it?"
    # So ppf(0.99) returns ~2.326, the z-score for the 99th percentile of a
    # standard normal distribution.
    z = stats.norm.ppf(confidence)
    # mu - z*sigma is the return at the confidence-level cutoff (the point on
    # the return distribution that separates the normal range from the tail)
    # on the fitted Gaussian: the mean shifted left by z standard deviations. It is negative
    # (a loss), so we negate it to return a positive loss fraction.
    return -(mu - z * sigma)


# ----------------------------------------------------------------------
# 3. Beta, CAPM (Capital Asset Pricing Model), risk decomposition (OLS of asset on market)
# - Beta (β) measures an asset's sensitivity to market moves: β = cov(asset_returns, market_returns) / var(market_returns),
#   the slope of asset return regressed on market return ("regressed on" = fitted as a straight
#   line with market return on the x-axis and asset return on the y-axis).
#   Beta is the regression slope coefficient when the return on the ith asset is regressed on the return on the market.
# - CAPM prices expected return as a linear function of beta: E[R_i] = R_f + β_i * (E[R_m] - R_f),
#   where R_f is the risk-free rate and (E[R_m] - R_f) is the market risk premium.
#   Intuition: investors are only compensated for non-diversifiable (market) risk, scaled by β.
# - R² measures how much of the asset's return variation is explained by the market's movements
#   (0 = no relation to market, 1 = moves in perfect lockstep). It is the square of the
#   correlation coefficient r from the regression.
# - Alpha (α) is the intercept of the regression line - the value of y (asset return) when
#   x (market return) is zero. It represents the return the asset earns above or below what
#   CAPM predicts given its beta: positive alpha means the asset outperformed the
#   market-implied expectation; negative means it underperformed.
# ----------------------------------------------------------------------
def regression_stats(asset_returns: pd.Series, market_returns: pd.Series) -> dict:
    """Regress asset excess return on market excess return.
    Returns alpha, beta, residuals, and R^2 - beta is the slope, exactly
    the 'regression slope coefficient' definition from the notes."""
    # Align
    df = pd.concat([asset_returns, market_returns], axis=1).dropna()
    df.columns = ['asset', 'market']

    rf_per_period = RISK_FREE_ANNUAL / PERIODS_PER_YEAR
    x = df['market'] - rf_per_period  # market excess return
    y = df['asset']  - rf_per_period  # asset excess return

    slope, intercept, r, p, se = stats.linregress(x, y)
    fitted = intercept + slope * x
    resid = y - fitted
    return {
        'beta': slope,
        'alpha_per_period': intercept,
        'r_squared': r**2,
        'p_value': p,
        'std_err': se,
        'resid': resid,
        'asset_returns': df['asset'],
        'market_returns': df['market'],
    }


def capm_expected_return(beta: float, market_returns: pd.Series) -> float:
    """CAPM: E[R_i] = R_f + beta*(E[R_m]-R_f), annualised."""
    rf = RISK_FREE_ANNUAL
    mkt_annual = market_returns.mean() * PERIODS_PER_YEAR
    return rf + beta * (mkt_annual - rf)


def risk_decomposition(reg: dict) -> dict:
    """var(R_i) = beta^2 * var(R_m) + var(epsilon).
    Confirms the systematic + idiosyncratic split from the notes."""
    beta = reg['beta']
    variance_total = reg['asset_returns'].var(ddof=1)
    variance_market = reg['market_returns'].var(ddof=1)
    variance_systematic = beta**2 * variance_market
    variance_idiosyncratic = reg['resid'].var(ddof=1)
    return {
        'variance_total': variance_total,
        'variance_systematic': variance_systematic,
        'variance_idiosyncratic': variance_idiosyncratic,
        'reconstructed_total': variance_systematic + variance_idiosyncratic,
        'systematic_fraction': variance_systematic / (variance_systematic + variance_idiosyncratic),
    }


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main(
    assets: list[str] = typer.Option(default=[ASSET], help='Asset ticker(s) (e.g. QCI.DE NVD.DE)'),
    assets_fractions: list[float] = typer.Option(default=[], help='Portfolio weight per asset (e.g. 0.6 0.4); must sum to 1 and match number of assets. Omit for equal weights.'),
    market: str = typer.Option(default=MARKET, help='Market index ticker (e.g. ^GDAXI)'),
    begin: int = typer.Option(default=BEGIN, help='Begin year (inclusive)'),
    end: int = typer.Option(default=END, help='End year (inclusive)'),
    var_confidence: float = typer.Option(default=VAR_CONFIDENCE, help='VaR confidence level (e.g. 0.99 for 99%)'),
    portfolio_value: float = typer.Option(default=PORTFOLIO_VALUE, help='Portfolio value in currency units'),
):
    if assets_fractions:
        if len(assets_fractions) != len(assets):
            raise SystemExit(f'assets_fractions length ({len(assets_fractions)}) must match assets length ({len(assets)}).')
        if abs(sum(assets_fractions) - 1.0) > 1e-6:
            raise SystemExit(f'assets_fractions must sum to 1 (got {sum(assets_fractions):.6f}).')
        weights = np.array(assets_fractions)
    else:
        weights = np.full(len(assets), 1.0 / len(assets))
    print(f'Downloading {assets} and {market} (market)...')
    prices = load_prices([*assets, market], f'{begin}-01-01', f'{end}-12-31', INTERVAL)
    if prices.empty or prices.shape[1] < 2:
        raise SystemExit('No data returned. Check tickers/dates.')

    returns = prices_to_returns(prices)
    market_returns = returns[market]

    print(f'\nSample: {prices.index[0].date()} -> {prices.index[-1].date()}  '
          f'({len(returns)} return obs)\n')

    for asset in assets:
        asset_returns = returns[asset]
        print(f'\n{"="*70}')
        print(f'Asset: {asset}')
        print(f'{"="*70}')

        # ---- VaR ----
        hvar = historical_var(asset_returns, var_confidence)
        pvar = parametric_var(asset_returns, var_confidence)
        print(f'=== {int(var_confidence*100)}% 1-day VaR for {asset} ===')
        print(f'=== (On any day there is {100-int(var_confidence*100)}% probability that position of {portfolio_value:,.0f} in {asset} loses more than...) ===')
        print(f'  Historical: {hvar:7.4%}  -> {hvar*portfolio_value:,.0f} EUR '
              f'on {portfolio_value:,.0f}  (based on what actually happened)')
        print(f'  Parametric: {pvar:7.4%}  -> {pvar*portfolio_value:,.0f} EUR '
              f'on {portfolio_value:,.0f}  (based on a normal distribution fitted to the data)')
        print(f'  Gap: a much larger historical VaR indicates fat tails  '
              f'(extreme losses more frequent than the Gaussian predicts), '
              f'which is common for equities during crises.')

        # ---- Beta / CAPM ----
        reg = regression_stats(asset_returns, market_returns)
        print(f'\n=== Beta & CAPM ({asset} vs {market}) ===')
        print(f'  Beta (slope)        : {reg['beta']:.3f}  (measures an asset\'s sensitivity to market moves)')
        print(f'  Alpha (annualised)  : {reg['alpha_per_period']*PERIODS_PER_YEAR:.4%}  (return above what CAPM predicts; positive = outperformed)')
        print(f'  R^2                 : {reg['r_squared']:.3f}  (fraction of asset variance explained by the market)')
        print(f'  p-value (beta)      : {reg['p_value']:.2e}'
              f'  (probability that beta is zero by chance; low value e.g. <0.05 means the market relationship is statistically significant)')

        capm = capm_expected_return(reg['beta'], market_returns)
        print(f'  CAPM E[R] (annual)  : {capm:.4%}  (CAPM - Capital Asset Pricing Model - expected return)')

        # ---- Risk decomposition ----
        dec = risk_decomposition(reg)
        print(f'\n=== Risk decomposition: var(R) = beta^2*var(R_m) + var(epsilon) ===')
        print(f'  Total variance            : {dec['variance_total']:.3e}')
        print(f'  Systematic (market)       : {dec['variance_systematic']:.3e} '
              f'({dec['systematic_fraction']:.1%})'
              f'  (market-driven risk; cannot be diversified away)')
        print(f'  Idiosyncratic (residual)  : {dec['variance_idiosyncratic']:.3e} '
              f'({1-dec['systematic_fraction']:.1%})'
              f'  (asset-specific risk; diversifiable in a large portfolio)')
        print(f'  Reconstructed total       : {dec['reconstructed_total']:.3e}  '
              f'(should match total by definition)')
        print(f'\n  Annualised volatility  : {asset_returns.std(ddof=1)*np.sqrt(PERIODS_PER_YEAR):.2%}'
              f'  (standard deviation of daily returns scaled to a full year; a common summary of total risk)')

    # ---- Portfolio covariance ----
    if len(assets) > 1:
        assets_returns = returns[assets]
        cov_matrix = assets_returns.cov() * PERIODS_PER_YEAR
        portfolio_variance = weights @ cov_matrix.values @ weights
        portfolio_volatility = np.sqrt(portfolio_variance)
        print(f'\n{"="*70}')
        print(f'Portfolio ({", ".join(f"{asset} {weight:.0%}" for asset, weight in zip(assets, weights))})')
        print(f'{"="*70}')
        print(f'  Covariance matrix (annualised):\n{cov_matrix.to_string()}'
              f'\n  (covariance measures how much two assets move together: positive = move in the same'
              f' direction, negative = move in opposite directions, zero = independent.'
              f' Negative or low covariance between assets reduces portfolio variance below the weighted'
              f' average of individual variances - the mathematical basis of diversification)')
        print(f'\n  Portfolio variance   : {portfolio_variance:.3e}')
        print(f'  Portfolio volatility : {portfolio_volatility:.2%}'
              f'  (weighted combination of assets; lower than average of individual volatilities if assets are not perfectly correlated)')


# ----------------------------------------------------------------------
# Tests - run with: `cd utilities/scripts && uv run --with pytest --with quantstats --with pandas --with scipy --with numpy --with typer --with yfinance pytest trader.py -v && cd -`
# Verifies metrics against QuantStats equivalents.
#
# Convention difference: trader.py uses log returns; QuantStats uses simple
# (percentage) returns. For daily data the two are very close
# (log(1+r) ≈ r for small r), so comparisons use a 1e-3 absolute tolerance.
# ----------------------------------------------------------------------

_ATOL = 1e-3  # tolerance for log vs simple return approximation
_RNG = np.random.default_rng(42)


def _make_prices(n: int = 500, beta: float = 1.2, noise: float = 0.01) -> pd.DataFrame:
    """Synthetic daily prices with a known market beta."""
    dates = pd.bdate_range('2020-01-01', periods=n)
    market_returns = _RNG.normal(0.0004, 0.01, n)
    asset_returns = beta * market_returns + _RNG.normal(0, noise, n)
    market_prices = 100 * np.exp(np.cumsum(market_returns))
    asset_prices = 100 * np.exp(np.cumsum(asset_returns))
    return pd.DataFrame({'asset': asset_prices, 'market': market_prices}, index=dates)


@pytest.fixture(scope='module')
def _sample() -> dict[str, pd.Series]:
    prices = _make_prices()
    log_returns = prices_to_returns(prices)
    simple_returns = prices.pct_change().dropna()
    return {
        'log_asset': log_returns['asset'],
        'log_market': log_returns['market'],
        'simple_asset': simple_returns['asset'],
        'simple_market': simple_returns['market'],
    }


def test_historical_var(_sample: dict[str, pd.Series]) -> None:
    # QuantStats does not expose historical VaR directly; equivalent is the
    # empirical quantile of losses.
    ours = historical_var(_sample['simple_asset'], VAR_CONFIDENCE)
    qs_var = -_sample['simple_asset'].quantile(1 - VAR_CONFIDENCE)
    assert abs(ours - qs_var) < _ATOL


def test_parametric_var(_sample: dict[str, pd.Series]) -> None:
    # qs.stats.value_at_risk returns the return at the cutoff (negative = loss),
    # while our parametric_var returns a positive loss fraction, so we negate.
    ours = parametric_var(_sample['simple_asset'], VAR_CONFIDENCE)
    qs_var = -qs.stats.value_at_risk(_sample['simple_asset'], confidence=VAR_CONFIDENCE)
    assert abs(ours - qs_var) < _ATOL


def test_beta(_sample: dict[str, pd.Series]) -> None:
    # qs.stats.greeks returns alpha and beta; uses simple returns internally.
    reg = regression_stats(_sample['log_asset'], _sample['log_market'])
    qs_beta = qs.stats.greeks(_sample['simple_asset'], _sample['simple_market'])['beta']
    assert abs(reg['beta'] - qs_beta) < _ATOL


def test_annualised_volatility(_sample: dict[str, pd.Series]) -> None:
    # qs.stats.volatility annualises using sqrt(252) on simple returns.
    ours = _sample['log_asset'].std(ddof=1) * np.sqrt(PERIODS_PER_YEAR)
    qs_vol = qs.stats.volatility(_sample['simple_asset'], periods=PERIODS_PER_YEAR)
    assert abs(ours - qs_vol) < _ATOL


def test_risk_decomposition_identity(_sample: dict[str, pd.Series]) -> None:
    # Mathematical identity: systematic + idiosyncratic must equal total variance.
    # Independent of any external package.
    reg = regression_stats(_sample['log_asset'], _sample['log_market'])
    dec = risk_decomposition(reg)
    assert abs(dec['variance_total'] - dec['reconstructed_total']) < 1e-10


if __name__ == '__main__':
    typer.run(main)