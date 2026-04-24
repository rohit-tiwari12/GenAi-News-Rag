import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure required NLTK data is available
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

# Initialize analyzer
sia = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str):
    score = sia.polarity_scores(text)["compound"]

    sentiment = (
        "positive" if score > 0.05 else
        "negative" if score < -0.05 else
        "neutral"
    )

    return sentiment, score