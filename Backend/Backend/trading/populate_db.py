# not needed for the app, it's just to manually add rows

from trading.models import Stock
import json
from django.db import IntegrityError

def to_float(value):
    try:
        return float(value) if value not in (None, "", "n/a") else None
    except ValueError:
        return None

def to_int(value):
    try:
        return int(float(value)) if value not in (None, "", "n/a") else None
    except ValueError:
        return None

def strip_dollar(value):
    return value[1:] if value and value.startswith("$") else value

def populate_stocks(json_path):
  count=0
  with open(json_path) as f:
    # loads into a list of dictionaries
    data = json.load(f)

  for item in data:
    stock = Stock(
      symbol=item.get('symbol'),
      company=item.get('name'),
      last_sale=to_float(strip_dollar(item.get('lastsale'))),
      volume=to_int(item.get('volume')),
      market_cap=to_int(item.get('marketCap')),
      country=item.get('country'),
      ipo_year=to_int(item.get('ipoyear')),
      industry=item.get('industry'),
      sector=item.get('sector'))
    try:
      stock.save()
    except IntegrityError:
      count+=1
  print(count)

populate_stocks('trading/nasdaq_full_tickers.json')