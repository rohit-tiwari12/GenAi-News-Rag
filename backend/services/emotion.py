def detect_emotion(text: str):
    text = text.lower()
    if any(word in text for word in ["fear", "concern", "decline", "loss"]):
        return "fear"
    if any(word in text for word in ["gain", "growth", "positive", "profit"]):
        return "joy"
    return "neutral"
