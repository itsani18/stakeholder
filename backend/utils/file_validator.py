from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = [".csv", ".txt"]


def validate_file(file: UploadFile):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File must have a name"
        )

    valid = any(
        file.filename.endswith(ext)
        for ext in ALLOWED_EXTENSIONS
    )

    if not valid:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and TXT files are allowed"
        )