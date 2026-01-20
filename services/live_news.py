import os
import requests
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def fetch_live_news(keyword="india", max_articles=5):
    if not GNEWS_API_KEY:
        raise ValueError("GNEWS_API_KEY is missing")

    url = "https://gnews.io/api/v4/search"
    params = {
        "q": keyword,
        "lang": "en",
        "country": "in",
        "max": max_articles,
        "apikey": GNEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise RuntimeError(f"GNews API request failed: {str(e)}")

    if "errors" in data:
        raise RuntimeError(f"GNews API error: {data['errors']}")

    articles = []
    for item in data.get("articles", []):
        articles.append({
            "title": item.get("title"),
            "content": item.get("description") or item.get("content") or "",
            "company": keyword,
            "date": (item.get("publishedAt") or "")[:10]
        })

    return articles
