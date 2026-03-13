import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY is missing in .env file")


def fetch_live_news(keyword="AI", max_articles=5):
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": keyword,
        "language": "en",
        "pageSize": max_articles,
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except Exception as e:
        raise RuntimeError(f"NewsAPI request failed: {str(e)}")

    articles = []

    for item in data.get("articles", []):
        text = (
            item.get("content")
            or item.get("description")
            or item.get("title")
            or ""
        )

        if not text.strip():
            continue

        articles.append({
            "title": item.get("title"),
            "content": text,
            "company": keyword,
            "date": (item.get("publishedAt") or "")[:10]
        })

    print(f"Fetched {len(articles)} articles from NewsAPI")

    return articles