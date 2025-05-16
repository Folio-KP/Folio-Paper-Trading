import yfinance as yf
from datetime import datetime, timedelta, timezone
import pandas as pd
import numpy as np

def safe_round(val):
    return round(val, 2) if isinstance(val, (int, float)) else None

def get_stock_info(symbol):
  ticker = yf.Ticker(symbol)

  try:
    info = ticker.info
  except Exception as e:
    info = {}

  stock_info = {}
  
  stock_info['last_sale'] = safe_round(info.get('regularMarketPrice'))
  stock_info['high'] = safe_round(info.get('dayHigh'))
  stock_info['low'] = safe_round(info.get('dayLow'))
  stock_info['open'] = safe_round(info.get('open'))
  stock_info['pe_ratio'] = safe_round(info.get('trailingPE'))
  stock_info['dividend_yield'] = safe_round(info.get('dividendYield'))
  stock_info['volume'] = safe_round(info.get('volume'))
  stock_info['market_cap'] = safe_round(info.get('marketCap'))
  stock_info['revenue'] = safe_round(info.get('totalRevenue'))
  stock_info['debt'] = safe_round(info.get('totalDebt'))

  return stock_info

# quick way to get the stock price (not really much faster)
def get_fast_price(symbol):
  ticker = yf.Ticker(symbol)
  try:
    price = ticker.fast_info['last_price']
  except Exception as e:
    price = None 
  return price


# Get historical data across standard intervals
def get_history_old(symbol):
    ticker = yf.Ticker(symbol)
    now = datetime.now(timezone.utc)

    intervals = {
        "1mo": now - timedelta(days=30),
        "5mo": now - timedelta(days=30 * 5),
        "1y": now - timedelta(days=365),
        "5y": now - timedelta(days=365 * 5),
        "max": None
    }

    results = {}

    for key, target_date in intervals.items():
        try:
            hist = ticker.history(period="max", interval="1d")
            if hist.empty:
                raise ValueError("No historical data available.")
            
            hist.index = pd.to_datetime(hist.index).tz_convert("UTC")

            if key == "max":
                oldest = hist.iloc[0]
                results[key] = {
                    "date": hist.index[0].date().isoformat(),
                    "open": round(float(oldest["Open"]), 4),
                    "high": round(float(oldest["High"]), 4),
                    "low": round(float(oldest["Low"]), 4),
                    "close": round(float(oldest["Close"]), 4),
                    "volume": round(float(oldest["Volume"]), 4),
                }
            else:
                # Use numpy.abs instead of .abs()
                timediffs = np.abs((hist.index - target_date).total_seconds())
                closest_idx = timediffs.argmin()
                row = hist.iloc[closest_idx]

                results[key] = {
                    "date": hist.index[closest_idx].date().isoformat(),
                    "open": round(float(row["Open"]), 4),
                    "high": round(float(row["High"]), 4),
                    "low": round(float(row["Low"]), 4),
                    "close": round(float(row["Close"]), 4),
                    "volume": round(float(row["Volume"]), 4),
                }
        except Exception as e:
            results[key] = {"error": str(e)}

    return results

# periods: 1d, 1wk, 1mo, 3mo, 1y, 5y
def get_history(symbol, period):
    ticker = yf.Ticker(symbol)

    # key = period, value = interval
    periods = {
       "1d": "15m",
       "1wk": "1h",
       "1mo": "1d",
       "3mo": "1wk",
       "1y": "1wk",
       "5y": "1mo"
       }

    results = {}

    if period not in periods.keys():
       raise ValueError('Not a valid period')

    try:
        hist = ticker.history(period=period, interval=periods[period])
        if hist.empty:
            raise ValueError("No historical data available.")

        # tz_localize removes timezone part of the datetime - assume ET
        results['date'] = list(hist.index.tz_localize(None).strftime("%Y-%m-%d %H:%M:%S").astype(str))
        results['price'] = list(round(hist['Close'],2))
    except Exception as e:
        results['date'] = []
        results['price'] = []

    return results