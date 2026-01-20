# 🧠 NewsMind AI  
### GenAI-Powered Live News Intelligence & RAG System

NewsMind AI is an end-to-end **GenAI application** that ingests live news, performs **sentiment and emotion analysis**, and enables **Retrieval-Augmented Generation (RAG)** based question answering using real-world data.

The system helps users go beyond headlines and **ask natural-language questions grounded in current news**.

---

## 🚀 Key Features

- 🔴 **Live News Ingestion** using external APIs  
- 😊 **Sentiment & Emotion Analysis** on news articles  
- 🧠 **Vector Search with FAISS** for semantic retrieval  
- 💬 **RAG-based Question Answering** powered by LLMs  
- 📊 **Interactive Streamlit Dashboard** with sentiment charts  
- 🔐 Secure API key handling using environment variables  

---

## 🧩 System Workflow

1. User selects a topic (e.g. *Tata Motors*)
2. System fetches live news articles
3. News is analyzed for sentiment & emotion
4. Articles are embedded into a vector store
5. User asks questions in natural language
6. LLM generates **grounded answers using retrieved context**

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend API | FastAPI |
| Frontend | Streamlit |
| LLM | Groq |
| Vector Store | FAISS |
| NLP | Sentence-Transformers, NLTK |
| Language | Python |

---

## ▶️ How to Run Locally (Without Docker)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/rohit-tiwari12/GenAi-News-Rag.git
cd GenAi-News-Rag


2️⃣ Create virtual environment

python -m venv venv
venv\Scripts\activate


3️⃣ Install dependencies
pip install -r requirements.txt
python -m nltk.downloader vader_lexicon



4️⃣ Set environment variables

Create a .env file in the root directory:

GROQ_API_KEY=your_groq_api_key
GNEWS_API_KEY=your_news_api_key


Run Backend (FastAPI)

uvicorn main:app --reload
http://127.0.0.1:8000/docs


Run Frontend (Streamlit)

streamlit run streamlit_app.py
http://localhost:8501



Example User Questions

Why is Tata Motors sentiment negative today?

Summarize today’s market news

What events caused fear in the auto sector?



📌 Use Cases

Market sentiment analysis

News intelligence dashboards

Analyst research tools

GenAI portfolio project



🧠 What This Project Demonstrates

End-to-end GenAI system design

Practical use of RAG architecture

API-based ML pipelines

Frontend-backend integration

Secure handling of secrets

Production-ready project structure



📈 Future Improvements

Database persistence (PostgreSQL)

Time-series sentiment trends

Chat history & user sessions

Cloud deployment (GCP / AWS)

Authentication & role-based access



👤 Author

Rohit Tiwari
⭐ If you find this project useful, consider starring the repository!
