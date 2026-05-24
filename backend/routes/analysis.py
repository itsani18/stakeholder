from fastapi import APIRouter

from db.repository import get_raw_feedback
from db.repository import save_analysis_result
from services.ml_predictor import predict_sentiment
from services.ml_predictor import predict_emotion
from services.summarizer import generate_summary
from services.topic_model import extract_topics
from services.keyword_extractor import extract_keywords
from services.wordcloud import generate_wordcloud


router = APIRouter()


@router.post("/analyze/{upload_id}")
async def analyze_feedback(upload_id: str):

    comments = get_raw_feedback(upload_id)

    sentiments = predict_sentiment(comments)

    emotions = predict_emotion(comments)

    summary = generate_summary(comments)

    topics = extract_topics(comments)

    keywords = extract_keywords(comments)

    generated_path = generate_wordcloud(comments)

    wordcloud_path = (
        "http://127.0.0.1:8000/generated/wordclouds/wordcloud.png"
    )

    result = {

        "upload_id": upload_id,

        "summary": summary,

        "topics": topics,

        "keywords": keywords,

        "wordcloud_path": wordcloud_path,

        "sentiments": sentiments,

        "emotions": emotions,
    }

    analysis_id = save_analysis_result(result)

    return {

        "message": "Analysis completed successfully",

        "analysis_id": analysis_id,

        "summary": summary,

        "topics": topics,

        "keywords": keywords,

        "wordcloud_url": wordcloud_path,

        "sentiments": sentiments,

        "emotions": emotions
    }