import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "https://newsmind-ai-backend.onrender.com"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="GenAI News Intelligence",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #0f172a;
}
.subtitle {
    color: #64748b;
    font-size: 16px;
    margin-bottom: 20px;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.metric-card {
    background: linear-gradient(135deg, #6366f1, #3b82f6);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🧠 GenAI News Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time News • Sentiment Analysis • AI-powered Q&A</div>', unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns([3,1])

with col1:
    keyword = st.text_input(
        "🔍 Enter a topic",
        placeholder="e.g. Tesla, AI, Stock Market"
    )

with col2:
    fetch_btn = st.button("🚀 Analyze")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PROCESS ----------------
if fetch_btn:
    if not keyword:
        st.warning("Please enter a topic first.")
    else:
        progress = st.progress(0)

        with st.spinner("Fetching live news..."):
            requests.post(f"{API_BASE_URL}/ingest/live", json={"keyword": keyword})
            progress.progress(30)

        with st.spinner("Analyzing sentiment..."):
            requests.post(f"{API_BASE_URL}/analyze")
            progress.progress(60)

        with st.spinner("Creating embeddings..."):
            requests.post(f"{API_BASE_URL}/embed")
            progress.progress(80)

        with st.spinner("Loading results..."):
            news_resp = requests.get(f"{API_BASE_URL}/news")
            progress.progress(100)

        if news_resp.status_code == 200:
            data = news_resp.json().get("data", [])

            if data:
                df = pd.DataFrame(data)

                st.success("✅ Analysis completed")

                # ---------------- KPI CARDS ----------------
                c1, c2, c3, c4 = st.columns(4)

                c1.markdown(f'<div class="metric-card">📰<br>{len(df)}<br>Total News</div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="metric-card">😊<br>{(df["sentiment"]=="positive").sum()}<br>Positive</div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="metric-card">😡<br>{(df["sentiment"]=="negative").sum()}<br>Negative</div>', unsafe_allow_html=True)
                c4.markdown(f'<div class="metric-card">😐<br>{(df["sentiment"]=="neutral").sum()}<br>Neutral</div>', unsafe_allow_html=True)

                # ---------------- CHART + TABLE ----------------
                col1, col2 = st.columns([1,1])

                with col1:
                    st.markdown("### 📊 Sentiment Distribution")
                    st.bar_chart(df["sentiment"].value_counts())

                with col2:
                    st.markdown("### 😊 Emotion Overview")
                    st.dataframe(df[["title", "sentiment", "emotion"]], use_container_width=True)

            else:
                st.warning("No news data available.")
        else:
            st.error("Failed to fetch processed data")

# ---------------- CHAT SECTION ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("### 💬 Ask AI")

question = st.text_input(
    "Ask a question",
    placeholder="What is happening in AI news?"
)

if st.button("💡 Get Answer"):
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("🤖 Generating answer..."):
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={"question": question}
            )

        if response.status_code == 200:
            result = response.json()

            if "answer" in result:
                st.markdown("### 🧠 AI Answer")
                st.success(result["answer"])
            else:
                st.error(result.get("error", "Something went wrong"))
        else:
            st.error("Chat request failed")

st.markdown('</div>', unsafe_allow_html=True)