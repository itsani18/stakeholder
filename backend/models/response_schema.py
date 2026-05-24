from pydantic import BaseModel

from typing import List


class UploadResponse(BaseModel):

    message: str

    total_comments: int

    inserted_ids: List[str]


class AnalysisResponse(BaseModel):

    message: str

    analysis_id: str

    summary: str

    topics: List[str]

    keywords: List[str]

    sentiments: List[str]

    wordcloud_path: str