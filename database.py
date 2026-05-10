import sqlite3
from datetime import datetime
DB_NAME = "market_advisor.db"



def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        price REAL NOT NULL,
        change_pct REAL NOT NULL,
        week_high REAL NOT NULL,
        week_low REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )   
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            headline TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            score REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )  
    """)

    conn.commit()
    conn.close()


def save_price_snapshot(ticker, price_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO price_snapshots (ticker, price, change_pct, week_high, week_low)
        VALUES (?, ?, ?, ?, ?)
        """, (
            ticker,
            price_data['price'],
            price_data['change_pct'],
            price_data['52_week_high'],
            price_data['52_week_low']
        ))
    conn.commit()
    conn.close()

def save_sentiment_score(ticker, sentiment_data):
    conn = get_connection()
    cursor = conn.cursor()

    for article in sentiment_data:
        cursor.execute("""
            INSERT INTO sentiment_scores (ticker, headline, sentiment, score)
            VALUES (?, ?, ?, ?)
            """, (
                ticker,
                article['title'],
                article['sentiment'],
                article['score']
            ))
        
    conn.commit()
    conn.close()
    
def get_price_history(ticker):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ticker,price, change_pct, timestamp
        FROM price_snapshots
        WHERE ticker = ?
        ORDER BY timestamp DESC
        LIMIT 10
        """, (ticker,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_sentiment_history(ticker):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ticker, sentiment, COUNT(*) as count,
            ROUND(AVG(score),2) as avg_score, timestamp
        FROM sentiment_scores
        WHERE ticker = ?
        GROUP BY DATE(timestamp), sentiment
        ORDER BY timestamp DESC
        LIMIT 20
    """, (ticker,))
        
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully")
    
    print("\nTSLA Price History:")
    history = get_price_history('TSLA')
    for row in history:
        print(row)

    print ("\nTSLA Sentiment History:")
    sentiment = get_sentiment_history('TSLA')
    for row in sentiment :
        print(row)