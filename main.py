from fastapi import FastAPI
from dotenv import load_dotenv

from services.sentiment import analyze_sentiment
from services.emotion import detect_emotion
from services.vector_store import VectorStore
from services.rag import generate_answer
from services.live_news import fetch_live_news

# Load environment variables
load_dotenv()

app = FastAPI(title="GenAI News RAG API (Groq + Live News)")

# In-memory storage
NEWS_DB = []
VECTOR_DB = VectorStore()


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "GenAI News RAG API is running"}


# ---------------- INGEST MANUAL NEWS ----------------
@app.post("/ingest")
def ingest(news: dict):
    """
    Ingest manual news article
    """
    NEWS_DB.append(news)
    return {
        "status": "news ingested",
        "count": len(NEWS_DB)
    }


# ---------------- INGEST LIVE NEWS ----------------
@app.post("/ingest/live")
def ingest_live_news(query: dict):
    """
    Fetch and ingest live news using GNews API
    """
    try:
        keyword = query.get("keyword", "india")
        articles = fetch_live_news(keyword)

        if not articles:
            return {"error": "No live news found"}

        NEWS_DB.extend(articles)

        return {
            "status": "live news ingested",
            "keyword": keyword,
            "count": len(articles)
        }

    except Exception as e:
        return {
            "error": "Live news ingestion failed",
            "details": str(e)
        }


# ---------------- ANALYZE NEWS ----------------
@app.post("/analyze")
def analyze():
    """
    Perform sentiment & emotion analysis
    """
    if not NEWS_DB:
        return {"error": "No news found. Please ingest news first."}

    for item in NEWS_DB:
        sentiment, score = analyze_sentiment(item["content"])
        item["sentiment"] = sentiment
        item["sentiment_score"] = score
        item["emotion"] = detect_emotion(item["content"])

    return {
        "status": "analysis completed",
        "data": NEWS_DB
    }


# ---------------- EMBED NEWS ----------------
@app.post("/embed")
def embed():
    """
    Embed news into FAISS vector store
    """
    if not NEWS_DB:
        return {"error": "No news available to embed."}

    VECTOR_DB.add_documents(NEWS_DB)
    return {"status": "documents embedded successfully"}


# ---------------- CHAT (RAG) ----------------
@app.post("/chat")
def chat(query: dict):
    """
    RAG-based question answering
    """
    try:
        question = query.get("question")
        if not question or not isinstance(question, str):
            return {
                "error": "Invalid request. Please provide a non-empty 'question' field."
            }

        results = VECTOR_DB.search(question)

        if not results:
            return {
                "error": "No documents found. Run /ingest → /analyze → /embed first."
            }

        answer = generate_answer(question, results)

        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:
        return {
            "error": "Chat service failed unexpectedly.",
            "details": str(e)
        }
