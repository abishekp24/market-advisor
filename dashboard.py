print("script started")
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")
import datetime
now = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")

watchlist = {
    'AAPL' : "Apple",
    'VOO' : "Vanguard S&P 500 ETF",
    'TSLA' : "Tesla",
    "D05.SI": "DBS Group",
    "ES3.SI": "STI ETF"
}

def get_signal (change_pct):
    if change_pct > 0.5:
        return "▲"
    elif change_pct < -0.5:
        return "▼"
    else :
        return "▬"

def fetch_quote(ticker):
    stock = yf.Ticker(ticker)
    info = stock.fast_info
    price = info.last_price
    prev_close = info.previous_close

    if price is None or prev_close is None:
        return None, None
    change_pct = ((price - prev_close) / prev_close) * 100
    return price, change_pct

print (f"== Your Market Dashboard ==\n")
print (f"Last updated: {now}\n")
       
for ticker,name in watchlist.items():
    price, change_pct = fetch_quote(ticker)
    if price is None:
        print(f"⚠️  {ticker:<10} Data unavailable ({name})")
    else:
        signal = get_signal(change_pct)
        print(f"{signal}  {ticker:<10} ${price:<10.2f} {change_pct:+.2f}%  ({name})")
