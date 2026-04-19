import warnings
import yfinance as yf

warnings.filterwarnings("ignore")

def get_price_snapshots (ticker):
    stock = yf.Ticker(ticker)
    info = stock.fast_info
    price = info.last_price
    prev_close = info.previous_close
    year_high = info.year_high
    year_low = info.year_low

    if price is None or prev_close is None:
        return None
    
    change_pct = ((price - prev_close) / prev_close) * 100

    return {
        "price": price,
        "change_pct": change_pct,
        "52_week_high": info.year_high,
        "52_week_low": info.year_low
    }

