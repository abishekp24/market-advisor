import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
from utils import get_price_snapshots

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

now = datetime.now().strftime("%d %b %Y, %I:%M %p")
print (f"== Your Market Dashboard ==\n")
print (f"Last updated: {now}\n")
       
for ticker,name in watchlist.items():
    data = get_price_snapshots(ticker)
    if data is None:
        print(f"⚠️  {ticker:<10} Data unavailable ({name})")
    else:
        signal = get_signal(data['change_pct'])
        print(f"{signal}  {ticker:<10} ${data['price']:<10.2f} {data['change_pct']:+.2f}%  ({name})")
