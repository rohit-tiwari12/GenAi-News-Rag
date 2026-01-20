import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="GenAI News Intelligence",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 GenAI News Intelligence Assistant")
st.write("Live news • Sentiment analysis • RAG-based Q&A")

# ---------------- STEP 1 ----------------
st.header("1️⃣ Choose a Topic")

keyword = st.text_input(
    "Enter a company / topic",
    placeholder="e.g. Tata Motors, Stock Market, AI"
)

# ---------------- STEP 2 ----------------
st.header("2️⃣ Fetch, Analyze & Visualize News")

if st.button("Fetch Live News"):
    if not keyword:
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Fetching live news..."):
            requests.post(
                f"{API_BASE_URL}/ingest/live",
                json={"keyword": keyword}
            )

        with st.spinner("Analyzing sentiment & emotion..."):
            analyze_resp = requests.post(f"{API_BASE_URL}/analyze")

        with st.spinner("Creating vector embeddings..."):
            requests.post(f"{API_BASE_URL}/embed")

        if analyze_resp.status_code == 200:
            data = analyze_resp.json().get("data", [])

            if data:
                df = pd.DataFrame(data)

                st.success("✅ Analysis completed")

                # -------- SENTIMENT CHART --------
                st.subheader("📊 Sentiment Distribution")

                sentiment_counts = df["sentiment"].value_counts()
                st.bar_chart(sentiment_counts)

                # -------- EMOTION TABLE --------
                st.subheader("😊 Emotion Overview")
                st.dataframe(df[["title", "sentiment", "emotion"]])

            else:
                st.warning("No news data available.")
        else:
            st.error("Failed to analyze news.")

# ---------------- STEP 3 ----------------
st.header("3️⃣ Ask Questions")

question = st.text_input(
    "Ask a question",
    placeholder="Why is sentiment negative today?"
)

if st.button("Ask"):
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json={"question": question}
            )

        if response.status_code == 200:
            result = response.json()
            if "answer" in result:
                st.markdown("### 💡 Answer")
                st.write(result["answer"])
            else:
                st.error(result.get("error", "Something went wrong"))
        else:
            st.error("Chat request failed")
