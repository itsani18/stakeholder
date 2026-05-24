from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from services.ingestion import process_uploaded_file
from utils.file_validator import validate_file

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    validate_file(file)

    result = await process_uploaded_file(file)

    return {

        "message": "File uploaded successfully",

        "upload_id": result["upload_id"],

        "total_comments": len(result["comments"]),

        "inserted_ids": [
            str(_id)
            for _id in result["inserted_ids"]
        ]
    }