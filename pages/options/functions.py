import numpy as np
from scipy.stats import norm
from datetime import datetime
import yfinance as yf
import pandas as pd
import math


class BSM_Greeks:

    def pdf(self, x):
        return math.exp(-(x**2) / 2) / math.sqrt(2 * math.pi)

    def cdf(self, x):
        return (1 + math.erf(x / math.sqrt(2))) / 2

    def d1(self, S, K, V, T):
        return (math.log(S / float(K)) + (V**2 / 2) * T) / (V * math.sqrt(T))

    def d2(self, S, K, V, T):
        return self.d1(S, K, V, T) - (V * math.sqrt(T))

    def theo(self, S, K, V, T, dT):
        if dT == "call":
            return S * self.cdf(self.d1(S, K, V, T)) - K * self.cdf(self.d2(S, K, V, T))
        else:
            return K * self.cdf(-self.d2(S, K, V, T)) - S * self.cdf(
                -self.d1(S, K, V, T)
            )

    def delta(self, S, K, V, T, dT):
        if dT == "call":
            delta = self.cdf(self.d1(S, K, V, T))
        elif dT == "put":
            delta = self.cdf(self.d1(S, K, V, T)) - 1
        else:
            delta = 1
        return delta

    def vega(self, S, K, V, T):
        vega = (S * math.sqrt(T) * self.pdf(self.d1(S, K, V, T))) / 100
        return vega

    def theta(self, S, K, V, T):
        theta = -((S * V * self.pdf(self.d1(S, K, V, T))) / (2 * math.sqrt(T))) / 365
        return theta

    def gamma(self, S, K, V, T):
        gamma = self.pdf(self.d1(S, K, V, T)) / (S * V * math.sqrt(T))
        return gamma


def bs_formula(
    S: float, K: float, T: float, sigma: float, _type: str = "call", r: float = None
) -> float:
    if not r:
        r = get_r()

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if _type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif _type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise Exception("Wrong option type!")
    return float(price)

def get_r():
    irx = yf.Ticker("^IRX")
    data = irx.history(period="1d")  # or "1y", "max", etc.\
    r = data.tail().Close.values[0] / 100
    #r = 4.2230 / 100
    return float(r)


def get_last_price(ticker):
    data = ticker.history(period="1d")
    price = data.tail().Close.values[0]
    #price = 196.58
    return float(price)


def get_sigma(ticker):
    data = ticker.history(period="3mo")
    sigma = data.Close.apply(lambda x: np.log(x)).diff(1).std() * np.sqrt(252)
    #sigma = 0.4
    return float(sigma)


def get_vol_matrix(ticker):
    #print("Getting Vols")
    expirations = ticker.options
    iv_surface = {}
    for expiry in expirations:  # Limit to 5 expirations for speed
        calls = ticker.option_chain(expiry).calls
        iv_surface[expiry] = calls.set_index("strike")["impliedVolatility"]
    # Combine into a DataFrame: rows = strike, columns = expiry
    iv_df = pd.DataFrame(iv_surface)
    iv_df = iv_df.sort_index()

    # Interpolate (within range only), fill extrapolated NaNs with nearest known value
    iv_df_filled = iv_df.interpolate(method="linear", axis=0)

    # Fill remaining NaNs at the top/bottom (extrapolation area) with nearest valid value
    iv_df_filled = iv_df_filled.fillna(method="bfill")  # Fill downward first
    iv_df_filled = iv_df_filled.fillna(method="ffill")  # Then fill upward

    last_price = get_last_price(ticker)

    return iv_df_filled.query(f"strike<={last_price*1.5} & strike>={last_price*0.5} ")
