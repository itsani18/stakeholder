import matplotlib
matplotlib.use("Agg")
import csv
import json
import math
import pickle
import re
import warnings
import os
import base64
from io import BytesIO

from collections import Counter, defaultdict
from io import StringIO
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wordcloud import WordCloud

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR

VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"

SENTIMENT_MODEL_PATH = MODEL_DIR / "sentiment_model.pkl"

EMOTION_MODEL_PATH = MODEL_DIR / "emotion_model.pkl"


SENTIMENT_LABELS = {

    0: "negative",

    1: "neutral",

    2: "positive",
}


EMOTION_LABELS = {

    0: "sadness",

    1: "anger",

    2: "joy",
}


STOP_WORDS = {

    "a", "about", "after", "all", "also", "am", "an", "and", "are", "as", "at", "be",
    "because", "been", "but", "by", "can", "could", "did", "do", "does", "for", "from",
    "had", "has", "have", "he", "her", "his", "i", "if", "in", "into", "is", "it", "its",
    "just", "more", "my", "no", "not", "of", "on", "or", "our", "out", "over", "so",
    "some", "still", "than", "that", "the", "their", "them", "there", "this", "to",
    "too", "us", "was", "we", "were", "what", "when", "with", "would", "you", "your",
}


THEME_DICTIONARY = {

    "Education": {
        "education", "students", "school",
        "learning", "teachers", "academic",
        "university", "training"
    },

    "Healthcare": {
        "healthcare", "hospital", "medical",
        "doctors", "patients", "treatment",
        "health", "medicine"
    },

    "Taxation and Economy": {
        "tax", "taxation", "economy",
        "economic", "business", "pricing",
        "cost", "investment", "financial"
    },

    "Technology and Digital Services": {
        "technology", "digital", "software",
        "platform", "system", "interface",
        "online", "automation"
    },

    "Communication": {
        "communication", "clarity", "clear",
        "unclear", "meeting", "message",
        "transparent", "discussion"
    },

    "Implementation and Execution": {
        "implementation", "execution",
        "rollout", "process", "deployment",
        "strategy", "delivery", "timeline"
    },

    "Support and Service": {
        "support", "response", "help",
        "ticket", "service", "contact",
        "resolved", "agent"
    },

    "Infrastructure and Transport": {
        "transport", "infrastructure",
        "roads", "railway", "traffic",
        "construction", "logistics",
        "development"
    },

    "Environment and Climate": {
        "environment", "climate",
        "pollution", "green",
        "sustainability", "emissions",
        "renewable", "ecology"
    },

    "Employment and Workforce": {
        "employment", "jobs",
        "workers", "salary",
        "career", "staff",
        "hiring", "workforce"
    },
}


POSITIVE_WORDS = {

    "accessible", "accurate", "adopted", "amazing",
    "appreciate", "beneficial", "best", "clear",
    "collaborative", "confident", "consistent",
    "delight", "easy", "effective", "efficient",
    "excellent", "fast", "good", "great",
    "helpful", "improved", "intuitive", "like",
    "love", "positive", "productive", "reliable",
    "responsive", "satisfied", "simple", "smooth",
    "strong", "successful", "supportive",
    "transparent", "useful", "valuable",
    "well", "happy", "excited",
}


NEGATIVE_WORDS = {

    "awful", "bad", "blocked", "broken", "bug",
    "confusing", "concern", "delay", "delayed",
    "difficult", "disappointed", "error",
    "expensive", "failed", "frustrating",
    "gap", "hard", "inconsistent", "issue",
    "late", "limited", "missing", "negative",
    "poor", "problem", "risk", "slow",
    "terrible", "unclear", "unhappy",
    "unreliable", "weak", "worse",
    "sad", "angry", "worried",
}


app = Flask(

    __name__,

    static_folder=str(BASE_DIR),

    static_url_path=""
)

CORS(app)


model_bundle = None

model_warning = None


def load_pickle(path):

    with warnings.catch_warnings(record=True) as caught:

        warnings.simplefilter("always")

        with path.open("rb") as file:

            value = pickle.load(file)

    return value, [str(warning.message) for warning in caught]


def load_models():

    global model_bundle, model_warning

    if model_bundle is not None:

        return model_bundle

    warnings_seen = []

    vectorizer, warnings_for_file = load_pickle(
        VECTORIZER_PATH
    )

    warnings_seen.extend(warnings_for_file)

    sentiment_model, warnings_for_file = load_pickle(
        SENTIMENT_MODEL_PATH
    )

    warnings_seen.extend(warnings_for_file)

    emotion_model, warnings_for_file = load_pickle(
        EMOTION_MODEL_PATH
    )

    warnings_seen.extend(warnings_for_file)

    model_warning = (
        " ".join(dict.fromkeys(warnings_seen))
        if warnings_seen
        else None
    )

    model_bundle = {

        "vectorizer": vectorizer,

        "sentiment": sentiment_model,

        "emotion": emotion_model,
    }

    return model_bundle


def tokenize(text):

    return [

        word.strip("-")

        for word in re.sub(
            r"[^a-zA-Z0-9\s-]",
            " ",
            text.lower()
        ).split()

        if len(word.strip("-")) > 2

        and word.strip("-") not in STOP_WORDS

        and not word.isdigit()
    ]


def detect_themes(comment):

    words = set(tokenize(comment))

    themes = [

        theme

        for theme, keywords in THEME_DICTIONARY.items()

        if words.intersection(keywords)
    ]

    return themes or ["General feedback"]


def label_for(raw_value, labels):

    try:

        key = int(raw_value)

    except (TypeError, ValueError):

        return str(raw_value).lower()

    return labels.get(key, f"class {key}")


def lexical_sentiment(comment):

    text = comment.lower()

    positive_hits = 0
    negative_hits = 0

    for word in POSITIVE_WORDS:

        if word in text:
            positive_hits += 1

    for word in NEGATIVE_WORDS:

        if word in text:
            negative_hits += 1

    # BOTH POSITIVE + NEGATIVE
    if positive_hits > 0 and negative_hits > 0:

        return "mixed", 0.85

    # POSITIVE
    if positive_hits > negative_hits:

        return "positive", 0.80

    # NEGATIVE
    if negative_hits > positive_hits:

        return "negative", 0.80

    # NEUTRAL
    return "neutral", 0.50


def calibrated_sentiment(comment, raw_label, proba_map):

    model_label = label_for(raw_label, SENTIMENT_LABELS)

    if not proba_map:

        return model_label, None, "model"

    ordered = sorted(
        proba_map.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_label, top_score = ordered[0]

    next_score = ordered[1][1] if len(ordered) > 1 else 0

    lexical_label, lexical_confidence = lexical_sentiment(comment)

    if lexical_label != "neutral":

        return lexical_label, lexical_confidence, "lexical"

    non_neutral = {

        label: score

        for label, score in proba_map.items()

        if label != "neutral"
    }

    best_non_neutral, best_non_neutral_score = max(
        non_neutral.items(),
        key=lambda item: item[1]
    )

    if lexical_label != "neutral" and (
        top_score - best_non_neutral_score <= 0.62
        or lexical_confidence >= 0.7
    ):

        return lexical_label, round(
            max(lexical_confidence, best_non_neutral_score),
            4
        ), "calibrated"

    if top_label == "neutral" and top_score < 0.62 and best_non_neutral_score > 0.30:

        return best_non_neutral, round(best_non_neutral_score, 4), "probability-adjusted"

    if top_score - next_score < 0.12:

        return "mixed", round(top_score, 4), "uncertain"

    return top_label, round(top_score, 4), "model"


def probabilities_for(model, matrix, labels):

    if not hasattr(model, "predict_proba"):

        return []

    classes = list(getattr(model, "classes_", []))

    probabilities = model.predict_proba(matrix)

    labelled = []

    for row in probabilities:

        labelled.append({

            label_for(class_id, labels): round(float(probability), 4)

            for class_id, probability in zip(classes, row)
        })

    return labelled


def confidence_for(proba_map):

    if not proba_map:

        return None

    return round(max(proba_map.values()), 4)


def clean_rows(rows):

    seen = set()

    cleaned = []

    for row in rows:

        comment = str(row.get("comment", "")).strip()

        group = str(row.get("group", "")).strip()

        key = comment.lower()

        if not comment or key in seen:

            continue

        seen.add(key)

        cleaned.append({

            "comment": comment,

            "group": group
        })

    return cleaned


def sentiment_counts(items):

    counts = {

        "positive": 0,

        "neutral": 0,

        "negative": 0,

        "mixed": 0
    }

    for item in items:

        counts[item["sentiment"]] = counts.get(
            item["sentiment"],
            0
        ) + 1

    return counts


def top_words(items, limit=20):

    counter = Counter()

    for item in items:

        counter.update(
            tokenize(item["comment"])
        )

    return [

        {
            "word": word,
            "count": count
        }

        for word, count in counter.most_common(limit)
    ]


def build_themes(items):

    themes = defaultdict(

        lambda: {

            "theme": "",

            "total": 0,

            "positive": 0,

            "neutral": 0,

            "negative": 0,

            "examples": [],
        }
    )

    for item in items:

        for theme in item["themes"]:

            current = themes[theme]

            current["theme"] = theme

            current["total"] += 1

            current[item["sentiment"]] = current.get(
                item["sentiment"],
                0
            ) + 1

            if len(current["examples"]) < 2:

                current["examples"].append(
                    item["comment"]
                )

    return sorted(

        themes.values(),

        key=lambda theme: theme["total"],

        reverse=True
    )

def build_summary(items, themes, words):

    if not items:
        return "No stakeholder comments were available for analysis."

    counts = sentiment_counts(items)

    positive = counts.get("positive", 0)
    negative = counts.get("negative", 0)
    neutral = counts.get("neutral", 0)
    mixed = counts.get("mixed", 0)

    total = len(items)

    positive_pct = round((positive / total) * 100)
    negative_pct = round((negative / total) * 100)
    neutral_pct = round((neutral / total) * 100)
    mixed_pct = round((mixed / total) * 100)

    # OVERALL REACTION
    if positive_pct >= 60:

        reaction = (
            "Stakeholders reacted very positively overall, "
            "with strong support for the proposal."
        )

    elif negative_pct >= 50:

        reaction = (
            "Stakeholders reacted negatively overall, "
            "with major concerns and dissatisfaction."
        )

    elif mixed_pct >= 40:

        reaction = (
            "Stakeholder reactions were highly mixed, "
            "showing both appreciation and criticism."
        )

    else:

        reaction = (
            "Stakeholder reactions were mostly neutral "
            "with moderate discussion and limited polarization."
        )

    # THEMES
    top_themes = [

        theme["theme"]

        for theme in themes[:3]
    ]

    if top_themes:

        theme_text = ", ".join(top_themes)

    else:

        theme_text = "general feedback"

    # KEYWORDS
    top_keywords = [

        word["word"]

        for word in words[:5]
    ]

    if top_keywords:

        keyword_text = ", ".join(top_keywords)

    else:

        keyword_text = "no major recurring terms"

    return (

        f"{reaction} "

        f"Out of {total} analyzed comments, "

        f"{positive_pct}% were positive, "

        f"{negative_pct}% were negative, "

        f"{neutral_pct}% were neutral, and "

        f"{mixed_pct}% were mixed. "

        f"The main discussion areas included {theme_text}. "

        f"Frequently recurring keywords were {keyword_text}."
    )


def generate_wordcloud(words):

    text = " ".join(words)

    wordcloud = WordCloud(

        width=1000,

        height=500,

        background_color="white"

    ).generate(text)

    plt.figure(figsize=(12, 6))

    plt.imshow(
        wordcloud,
        interpolation="bilinear"
    )

    plt.axis("off")

    buffer = BytesIO()

    plt.savefig(
        buffer,
        format="png",
        bbox_inches="tight"
    )

    buffer.seek(0)

    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    plt.close()

    return image_base64


def analyze_feedback(rows):

    cleaned = clean_rows(rows)

    if not cleaned:

        return {

            "items": [],

            "sentiment": {
                "positive": 0,
                "neutral": 0,
                "negative": 0,
                "mixed": 0
            },

            "themes": [],

            "words": [],

            "summary": "No comments were available for analysis.",

            "wordcloud_url": "",

            "modelWarning": model_warning,
        }

    bundle = load_models()

    comments = [

        row["comment"]

        for row in cleaned
    ]

    matrix = bundle["vectorizer"].transform(
        comments
    )

    sentiment_raw = bundle["sentiment"].predict(
        matrix
    )

    emotion_raw = bundle["emotion"].predict(
        matrix
    )

    sentiment_proba = probabilities_for(

        bundle["sentiment"],

        matrix,

        SENTIMENT_LABELS
    )

    emotion_proba = probabilities_for(

        bundle["emotion"],

        matrix,

        EMOTION_LABELS
    )

    items = []

    for index, row in enumerate(cleaned):

        sentiment_map = (

            sentiment_proba[index]

            if sentiment_proba

            else {}
        )

        sentiment, confidence, source = calibrated_sentiment(

            row["comment"],

            sentiment_raw[index],

            sentiment_map
        )

        if sentiment not in {

            "positive",
            "neutral",
            "negative",
            "mixed"
        }:

            sentiment = "neutral"

        item = {

            "id": index + 1,

            "comment": row["comment"],

            "group": row["group"],

            "sentiment": sentiment,

            "modelSentiment": label_for(
                sentiment_raw[index],
                SENTIMENT_LABELS
            ),

            "sentimentProbabilities": sentiment_map,

            "confidence": confidence,

            "sentimentSource": source,

            "emotion": label_for(
                emotion_raw[index],
                EMOTION_LABELS
            ),

            "emotionProbabilities": (
                emotion_proba[index]
                if emotion_proba
                else {}
            ),

            "emotionConfidence": (
                confidence_for(emotion_proba[index])
                if emotion_proba
                else None
            ),

            "themes": detect_themes(
                row["comment"]
            ),
        }

        items.append(item)

    themes = build_themes(items)

    words = top_words(items, 40)

    word_list = [

        word["word"]

        for word in words
    ]

    wordcloud_url = generate_wordcloud(
        word_list
    )

    return {

        "items": items,

        "sentiment": sentiment_counts(items),

        "themes": themes,

        "words": words,

        "summary": build_summary(
            items,
            themes,
            words
        ),

        "wordcloud": wordcloud_url,

        "modelWarning": model_warning,
    }


@app.get("/")
def index():

    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


@app.get("/api/health")
def health():

    load_models()

    return jsonify({

        "status": "ok",

        "models": {

            "vectorizer": str(VECTORIZER_PATH),

            "sentiment": str(SENTIMENT_MODEL_PATH),

            "emotion": str(EMOTION_MODEL_PATH),
        },

        "warning": model_warning,
    })


@app.post("/api/analyze")
def analyze():

    data = request.get_json(
        force=True,
        silent=True
    ) or {}

    rows = data.get("rows", [])

    if not isinstance(rows, list):

        return jsonify({
            "error": "rows must be a list"
        }), 400

    return jsonify(
        analyze_feedback(rows)
    )


@app.post("/api/analyze-file")
def analyze_file():

    upload = request.files.get("file")

    if not upload:

        return jsonify({
            "error": "file is required"
        }), 400

    text = upload.read().decode(
        "utf-8",
        errors="replace"
    )

    if upload.filename.lower().endswith(".csv"):

        reader = csv.DictReader(
            StringIO(text)
        )

        rows = []

        headers = reader.fieldnames or []

        comment_key = next(

            (
                key

                for key in headers

                if key.lower() in {
                    "comment",
                    "feedback",
                    "response",
                    "text",
                    "description"
                }
            ),

            headers[0] if headers else ""
        )

        group_key = next(

            (
                key

                for key in headers

                if key.lower() in {
                    "group",
                    "stakeholder",
                    "department",
                    "team",
                    "region"
                }
            ),

            ""
        )

        for record in reader:

            rows.append({

                "comment": record.get(
                    comment_key,
                    ""
                ),

                "group": record.get(
                    group_key,
                    ""
                ) if group_key else ""
            })

    else:

        rows = [

            {
                "comment": line,
                "group": ""
            }

            for line in text.splitlines()
        ]

    return jsonify(
        analyze_feedback(rows)
    )


@app.get("/generated/<path:filename>")
def generated_files(filename):

    return send_from_directory(
        "generated",
        filename
    )


@app.route("/generated/wordclouds/<filename>")
def generated_wordclouds(filename):

    return send_from_directory(
        BASE_DIR.parent / "generated" / "wordclouds",
        filename
    )


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )