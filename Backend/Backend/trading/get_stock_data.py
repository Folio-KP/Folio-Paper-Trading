import yfinance as yf

# get all the stock info needed to update database
def get_stock_info(symbol):
  ticker = yf.Ticker(symbol)

  try:
    info = ticker.info
  except Exception as e:
    info = {}

  stock_info = {}
  
  stock_info['last_sale'] =info.get('regularMarketPrice')
  stock_info['high'] =info.get('dayHigh')
  stock_info['low'] =info.get('dayLow')
  stock_info['open'] =info.get('open')
  stock_info['pe_ratio'] =info.get('trailingPE')
  stock_info['dividend_yield'] =info.get('dividendYield')
  stock_info['volume'] =info.get('volume')
  stock_info['market_cap'] =info.get('marketCap')
  stock_info['revenue'] =info.get('totalRevenue')
  stock_info['debt'] =info.get('totalDebt')

  return stock_info

# quick way to get the stock price (not really much faster)
def get_fast_price(symbol):
  ticker = yf.Ticker(symbol)
  try:
    price = ticker.fast_info['last_price']
  except Exception as e:
    price = None 
  return price

# get timeseries data and format as dictionary
# periods: 1d, 1wk, 1mo, 1y
def get_history(symbol, period):
  ticker = yf.Ticker(symbol)
  history = ticker.history(period=period)
  # format as json and return