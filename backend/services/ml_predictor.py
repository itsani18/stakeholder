import pickle
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "ml_models"


vectorizer = pickle.load(
    open(MODEL_DIR / "vectorizer.pkl", "rb")
)

sentiment_model = pickle.load(
    open(MODEL_DIR / "sentiment_model.pkl", "rb")
)

emotion_model = pickle.load(
    open(MODEL_DIR / "emotion_model.pkl", "rb")
)


print(sentiment_model.classes_)
print(emotion_model.classes_)


SENTIMENT_LABELS = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

EMOTION_LABELS = {
    0: "sadness",
    1: "anger",
    2: "joy"
}


def predict_sentiment(comments):

    vectors = vectorizer.transform(comments)

    predictions = sentiment_model.predict(vectors)

    results = []

    for comment, pred in zip(comments, predictions):

        results.append({
            "text": comment,
            "sentiment": SENTIMENT_LABELS.get(
                int(pred),
                str(pred)
            )
        })

    return results


def predict_emotion(comments):

    vectors = vectorizer.transform(comments)

    predictions = emotion_model.predict(vectors)

    results = []

    for comment, pred in zip(comments, predictions):

        results.append({
            "text": comment,
            "emotion": EMOTION_LABELS.get(
                int(pred),
                str(pred)
            )
        })

    return results


print(
    predict_sentiment(
        ["I love this policy"]
    )
)

print(
    predict_sentiment(
        ["This law is terrible"]
    )
)

print(
    predict_sentiment(
        ["This proposal is average"]
    )
)