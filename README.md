# Market Advisor Dashboard

## What it does
A personal market dashboard that pulls live price data for a 
customisable watchlist of US stocks, Singapore-listed stocks, 
and ETFs. Displays current price, percentage change from 
previous close, and a directional signal for each ticker.

## How it works
1. Reads a hardcoded watchlist of ticker symbols
2. Fetches live market data from the Yahoo Finance API 
   via yfinance (15 min delay)
3. Calculates percentage change between previous close 
   and current price
4. Displays a formatted dashboard with price, change %, 
   and a signal (▲ / ▼ / ▬) for each ticker

## Tech used
- Python 3.9
- yfinance 1.2.0 — market data from Yahoo Finance
- datetime — timestamp formatting

## How to run it

**1. Clone the repo**
git clone https://github.com/abishekp24/market-advisor.git
cd market-advisor

**2. Create and activate a virtual environment**
python3 -m venv venv
source venv/bin/activate

**3. Install dependencies**
pip install yfinance

**4. Run the dashboard**
python3 dashboard.py

## Roadmap
- [ ] Add Reddit sentiment analysis (r/investing, r/wallstreetbets)
- [ ] Store historical data in a local SQL database
- [ ] Track personal portfolio and calculate overall performance
- [ ] AI-powered investment advisor that synthesises price 
      trends, sentiment and global news into recommendations 