import os
import warnings
from datetime import datetime
from dotenv import load_dotenv
from utils import get_price_snapshots
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import  yfinance as yf
from groq import Groq
import sys


warnings.filterwarnings("ignore")
load_dotenv()
#api_key = os.getenv("GROQ_API_KEY")


def get_news_and_sentiment(ticker):
    stock = yf.Ticker(ticker)
    news =  stock.news

    analyzer = SentimentIntensityAnalyzer()
    results = []
    company_name = stock.info.get('longName',ticker)
    company_name = company_name.replace(', Inc.', '').replace(', Inc', '').strip()

    
    for article in news:
        
        title = article['content']['title'].replace('\xa0', ' ')
        summary = article['content'].get('summary', '')
      

        if ticker.upper() not in title.upper() and company_name.upper() not in title.upper():
            continue

        score =  analyzer.polarity_scores(title)
        compound = score['compound']

        if compound >= 0.05:
            sentiment = "Positive"

        elif compound <= -0.05:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

        results.append({
            "title": title,
            "sentiment": sentiment,
            "score": compound
        })

    return results
    
def get_ai_summary(ticker,price_data, sentiment_data):
    client = Groq(api_key = os.getenv("Groq_API_KEY"))
    positive = sum(1 for a in sentiment_data if a["sentiment"] == "Positive")
    negative = sum(1 for a in sentiment_data if a["sentiment"] == "Negative")
    neutral = sum(1 for a in sentiment_data if a["sentiment"] == "Neutral")
    avg_score = sum(a['score'] for a in sentiment_data) / len(sentiment_data) if sentiment_data else 0
    headlines = "\n".join([f"- {a['title']} ({a['sentiment']})" for a in sentiment_data])


    prompt = f"""
You are a market analyst. Provide a concise summary of the current state of {ticker} stock based on the following data:

Here is data for {ticker}:
PRICE : 
- Current Price: ${price_data['price']:.2f}
- Change Percentage: {price_data['change_pct']:+.2f}%
- 52 Week High: ${price_data['52_week_high']:.2f}
- 52 Week Low: ${price_data['52_week_low']:.2f}

NEWS SENTIMENT:
- Positive: {positive}, - Negative: {negative}, - Neutral: {neutral} neutral articles
- Average Sentiment Score: {avg_score:.2f}

Headlines:
{headlines}

Write a concise summary (2-3 sentences) of the current state of {ticker} stock based on the above data.
Cover : current price trend, overall market sentiment, any notable news impact and a cautious outlook.
Do not include any disclaimers or advice. Focus on providing an objective analysis based on the data provided.
"""
    
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


def run_research(ticker):
    ticker = ticker.upper()
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")
    print(f"\n{'='*50}")
    print(f"Researc Brief : {ticker}")
    print(f"Generated: {now}")
    print(f"{'='*50}")

    print("\nFetching price data...")
    price_data = get_price_snapshots(ticker)
    if price_data is None:
        print (f"Could not fetch price data for {{ticker}}")
        return
    
    print ("Fetching news and analyzing sentiment...")
    sentiment_data = get_news_and_sentiment(ticker)

    print ("Generating AI Summary...")
    summary = get_ai_summary (ticker,price_data,sentiment_data)

    print (f"\nPRICE SNAPSHOT")
    print (f"Current Price: ${price_data['price']:.2f}")
    print (f"Previous Close: ${price_data['price'] - (price_data['price'] * price_data['change_pct'] / 100):.2f}")
    print (f"Change: {price_data['change_pct']:+.2f}%")
    print (f"52 week high: ${price_data['52_week_high']:.2f}")
    print (f"52 week low: ${price_data['52_week_low']:.2f}")

    print (f"\nNEWS SENTIMENT ({len(sentiment_data)} articles)")
    for article in sentiment_data:
        icon = "✅" if article['sentiment'] == 'Positive' else "⚠️" if article['sentiment'] == 'Negative' else "➡️"
        print(f"{icon} {article['title'][:70]}")

    print(f"{icon} {article['title'][:70]}")

    print(f"\nAI Summary")
    print(summary)
    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "TSLA"
    run_research(ticker)