from wordcloud import WordCloud


def generate_wordcloud(comments):

    combined_text = " ".join(comments)

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(combined_text)

    output_path = "generated/wordclouds/wordcloud.png"

    wordcloud.to_file(output_path)

    return "/generated/wordclouds/wordcloud.png"