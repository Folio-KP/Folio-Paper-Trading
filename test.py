import yfinance as yf

symbol = "AAPL"
specific_date = "2025-01-02"

# Fetch data with a buffer range (e.g., 5 days before and after)
stock = yf.Ticker(symbol)
data = stock.history(start="2024-12-30", end="2025-01-02")

# Find the closest available trading day
if not data.empty:
    closest_date = data.index[-1].strftime("%Y-%m-%d")
    price_on_date = data["Close"].iloc[-1]
    print(f"Closest available trading day: {closest_date}, Price: ${price_on_date:.2f}")
else:
    print(f"No trading data available near {specific_date}")
