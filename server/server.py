from mcp.server.fastmcp import FastMCP
import requests
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Intelligent Tool System")



@mcp.tool()
def get_weather(city: str) -> dict:
    """Get the current weather for any city in the world."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "OpenWeather API key not found."}

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Could not find weather for '{city}'."}

    data = response.json()
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature_celsius": data["main"]["temp"],
        "feels_like_celsius": data["main"]["feels_like"],
        "condition": data["weather"][0]["description"],
        "humidity_percent": data["main"]["humidity"],
        "wind_speed_kmh": round(data["wind"]["speed"] * 3.6, 1)
    }

# ─── TOOL 2, 3, 4: EXPENSE TRACKER ───────────────────────────────────────────
# We store the database inside the server/ folder

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

def init_db():
    """Create the expenses table if it doesn't exist yet."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

# Run once when server starts
init_db()

@mcp.tool()
def add_expense(date: str, amount: float, category: str,
                subcategory: str = "", note: str = "") -> dict:
    """
    Add a new expense to the database.
    date format: YYYY-MM-DD  example: 2025-05-06
    amount: number  example: 250.00
    category: string  example: Food
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "added", "id": cur.lastrowid}

@mcp.tool()
def list_expenses(start_date: str, end_date: str) -> list:
    """
    List all expenses between two dates (inclusive).
    date format: YYYY-MM-DD  example: 2025-05-01 to 2025-05-31
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """SELECT id, date, amount, category, subcategory, note
               FROM expenses
               WHERE date BETWEEN ? AND ?
               ORDER BY date ASC""",
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

@mcp.tool()
def summarize_expenses(start_date: str, end_date: str,
                       category: str = "") -> list:
    """
    Show total spending grouped by category between two dates.
    Optionally filter by a specific category.
    """
    with sqlite3.connect(DB_PATH) as conn:
        query = """SELECT category, SUM(amount) AS total
                   FROM expenses
                   WHERE date BETWEEN ? AND ?"""
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY total DESC"

        cur = conn.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    
    # ─── TOOL 5: SENTIMENT ANALYSIS ───────────────────────────────────────────────
# We load the model once when the server starts (not on every request)
# This avoids a 10-second delay every time someone asks for sentiment

from transformers import pipeline

print("Loading sentiment model... (takes ~10 seconds first time)")
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
print("Sentiment model ready!")

@mcp.tool()
def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of any text.
    Returns whether it is POSITIVE or NEGATIVE and how confident the model is.
    Example: analyze_sentiment("I love this product!")
    """
    if not text or len(text.strip()) == 0:
        return {"error": "Please provide some text to analyze."}

    # The model only handles up to 512 tokens so we trim long text
    text = text[:1000]

    result = sentiment_model(text)[0]

    return {
        "text": text,
        "sentiment": result["label"],        # POSITIVE or NEGATIVE
        "confidence": round(result["score"] * 100, 2)  # e.g. 98.5%
    }

# ─── TOOL 6: CURRENCY CONVERTER ───────────────────────────────────────────────

@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Convert an amount from one currency to another using live exchange rates.
    Example: convert_currency(100, "USD", "INR")
    Use standard 3-letter currency codes: USD, INR, EUR, GBP, JPY, AED etc.
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        return {"error": "Exchange Rate API key not found in .env file."}

    # Make the currency codes uppercase so "usd" and "USD" both work
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    # Build the API URL
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Could not reach the currency API. Try again later."}

    data = response.json()

    # If the API returns an error (e.g. invalid currency code)
    if data.get("result") != "success":
        return {"error": f"Invalid currency code. Please use codes like USD, INR, EUR, GBP."}

    return {
        "from": f"{amount} {from_currency}",
        "to": f"{round(data['conversion_result'], 2)} {to_currency}",
        "exchange_rate": data["conversion_rate"],
        "last_updated": data["time_last_update_utc"]
    }
# ─── TOOL 7: NEWS SEARCH ──────────────────────────────────────────────────────

@mcp.tool()
def get_news(topic: str) -> list:
    """
    Get the latest 5 news headlines for any topic.
    Example: get_news("artificial intelligence")
    Example: get_news("cricket India")
    Example: get_news("stock market")
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return [{"error": "News API key not found in .env file."}]

    # Build the API URL
    # sortBy=publishedAt means we get the most recent articles first
    url = (
        f"https://newsapi.org/v2/everything"
        f"?q={topic}"
        f"&sortBy=publishedAt"
        f"&pageSize=5"
        f"&language=en"
        f"&apiKey={api_key}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return [{"error": "Could not reach the News API. Try again later."}]

    data = response.json()

    # If no articles found for this topic
    if not data.get("articles"):
        return [{"error": f"No news found for topic: '{topic}'"}]

    # Extract only the fields we care about from each article
    results = []
    for article in data["articles"]:
        results.append({
            "headline": article["title"],
            "source": article["source"]["name"],
            "description": article["description"],
            "url": article["url"],
            "published_at": article["publishedAt"]
        })

    return results

# ─── RUN THE SERVER ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")