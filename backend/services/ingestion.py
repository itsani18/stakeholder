import csv
import uuid

from utils.text_cleaner import clean_text
from db.repository import save_raw_feedback


async def process_uploaded_file(file):

    content = await file.read()

    decoded = content.decode("utf-8").splitlines()

    reader = csv.DictReader(decoded)

    upload_id = str(uuid.uuid4())

    documents = []

    for row in reader:

        comment = row.get("comment", "").strip()

        if not comment:
            continue

        cleaned_comment = clean_text(comment)

        document = {
            "upload_id": upload_id,
            "comment": cleaned_comment
        }

        documents.append(document)

    print(documents)
    print(type(documents))
    print(type(documents[0]))

    inserted_ids = save_raw_feedback(documents)

    return {
        "upload_id": upload_id,
        "comments": documents,
        "inserted_ids": inserted_ids
    }