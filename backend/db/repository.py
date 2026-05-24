from db.mongodb import raw_feedback_collection
from db.mongodb import analysis_collection
from bson import ObjectId


def save_raw_feedback(documents):

    result = raw_feedback_collection.insert_many(documents)

    return result.inserted_ids


def get_raw_feedback(upload_id):

    comments = list(raw_feedback_collection.find())

    print(comments)

    return [
        item["comment"]
        for item in comments
        if item["upload_id"] == upload_id
    ]


def save_analysis_result(result):

    response = analysis_collection.insert_one(result)

    return str(response.inserted_id)


def get_analysis_result(analysis_id):

    result = analysis_collection.find_one({
        "_id": ObjectId(analysis_id)
    })

    if result:
        result["_id"] = str(result["_id"])

    return result