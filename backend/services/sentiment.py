from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    score = sia.polarity_scores(text)["compound"]
    sentiment = (
        "positive" if score > 0.05 else
        "negative" if score < -0.05 else
        "neutral"
    )
    return sentiment, score
