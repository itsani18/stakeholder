from collections import Counter


def generate_summary(comments):

    if not comments:
        return "No comments available"

    combined = " ".join(comments)

    words = combined.split()

    common_words = Counter(words).most_common(10)

    summary = "Top discussed words: "

    summary += ", ".join(
        [word for word, _ in common_words]
    )

    return summary