from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from services.sentiment import analyze_sentiment
from services.emotion import detect_emotion
from services.vector_store import VectorStore
from services.rag import generate_answer
from services.live_news import fetch_live_news

# Load environment variables
load_dotenv()

# Initialize app
app = FastAPI(title="GenAI News RAG API (Groq + Live News)")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- GLOBAL STORAGE ----------------
NEWS_DB = []
VECTOR_DB = VectorStore()


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "GenAI News RAG API is running 🚀"}


# ---------------- HEALTH ----------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------- GET ALL NEWS (NEW - IMPORTANT) ----------------
@app.get("/news")
def get_news():
    return {
        "count": len(NEWS_DB),
        "data": NEWS_DB
    }


# ---------------- RESET (OPTIONAL - DEBUGGING) ----------------
@app.post("/reset")
def reset():
    NEWS_DB.clear()
    global VECTOR_DB
    VECTOR_DB = VectorStore()
    return {"status": "reset successful"}


# ---------------- INGEST MANUAL NEWS ----------------
@app.post("/ingest")
def ingest(news: dict):
    NEWS_DB.append(news)
    return {
        "status": "news ingested",
        "count": len(NEWS_DB)
    }


# ---------------- INGEST LIVE NEWS ----------------
@app.post("/ingest/live")
def ingest_live_news(query: dict):
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
    if not NEWS_DB:
        return {"error": "No news found. Please ingest news first."}

    for item in NEWS_DB:
        text = item.get("content") or item.get("title", "")

        sentiment, score = analyze_sentiment(text)
        item["sentiment"] = sentiment
        item["sentiment_score"] = score
        item["emotion"] = detect_emotion(text)

    return {
        "status": "analysis completed",
        "count": len(NEWS_DB)
    }


# ---------------- EMBED NEWS ----------------
@app.post("/embed")
def embed():
    if not NEWS_DB:
        return {"error": "No news available to embed."}

    valid_docs = []

    for item in NEWS_DB:
        text = item.get("content") or item.get("title")
        if text:
            valid_docs.append({
                "content": text,
                "metadata": {
                    "title": item.get("title"),
                    "date": item.get("date"),
                    "company": item.get("company")
                }
            })

    if not valid_docs:
        return {"error": "No valid documents to embed."}

    VECTOR_DB.add_documents(valid_docs)

    return {
        "status": "documents embedded successfully",
        "count": len(valid_docs)
    }


# ---------------- CHAT (RAG) ----------------
@app.post("/chat")
def chat(query: dict):
    try:
        question = query.get("question")

        if not question or not isinstance(question, str):
            return {"error": "Provide valid 'question'"}

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
            "error": "Chat failed",
            "details": str(e)
        }