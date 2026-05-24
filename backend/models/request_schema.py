from pydantic import BaseModel


class AnalyzeRequest(BaseModel):

    upload_id: str