from collections import Counter


def extract_topics(comments):

    combined = " ".join(comments)

    words = combined.split()

    stopwords = {
        "is",
        "the",
        "a",
        "an",
        "too",
        "very"
    }

    filtered_words = [
        word
        for word in words
        if word not in stopwords
    ]

    common_words = Counter(filtered_words).most_common(5)

    topics = [
        word
        for word, _ in common_words
    ]

    return topics