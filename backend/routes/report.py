from fastapi import APIRouter
from bson import ObjectId

from db.mongodb import analysis_collection

router = APIRouter()


@router.get("/report/{analysis_id}")
async def generate_report(analysis_id: str):

    report = analysis_collection.find_one({
        "_id": ObjectId(analysis_id)
    })

    if not report:
        return {
            "message": "Report not found"
        }

    report["_id"] = str(report["_id"])

    return report