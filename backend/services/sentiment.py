def analyze_sentiment(comments):

    positive_words = [
        "great",
        "excellent",
        "good",
        "awesome",
        "happy",
        "love"
    ]

    negative_words = [
        "bad",
        "unfair",
        "harsh",
        "poor",
        "terrible",
        "worst"
    ]

    results = []

    for comment in comments:

        text = comment.lower()

        sentiment = "neutral"

        if any(word in text for word in positive_words):
            sentiment = "positive"

        if any(word in text for word in negative_words):
            sentiment = "negative"

        results.append({
            "text": comment,
            "sentiment": sentiment
        })

    return results