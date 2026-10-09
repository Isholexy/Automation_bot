import csv
from io import StringIO

from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from chunker import chunk_recipients
from engine import dispatch_broadcast
from validator import sanitize_phone_list

app = FastAPI(title="SMS Broadcast API",)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "Online", "message": "Broadcasting API is running "}

@app.post("/broadcast/csv")
async def broadcast_via_csv(
        message: str = Form(..., description="The message to broadcast"),
        default_region: str = Form("US", description="Default region for phone number validation"),
        file: UploadFile = File(..., description="CSV file containing phone numbers"),
) -> dict:
    """
    Accepts a CSV file upload containing phone numbers, validates and normalizes them,
    chunks them into batches, and dispatches the broadcast message to all valid numbers.
    """
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    # 1. Read and decode the uploaded CSV file content in memory
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.reader(StringIO(decoded))

    raw_extracted_numbers: list[str] = []
    for row in reader:
        if row and row[0].strip():
            # Grabs the first column of each row
            raw_extracted_numbers.append(row[0].strip())

    if not raw_extracted_numbers:
        raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")

    # 2. Step A: Run through validator.py
    valid_numbers, invalid_numbers = sanitize_phone_list(
        raw_extracted_numbers, default_region=default_region
    )

    if not valid_numbers:
        raise HTTPException(
            status_code=400, 
            detail="No valid phone numbers could be extracted from the CSV file."
        )

    # 3. Step B: Run through chunker.py (batches of 100)
    batches = chunk_recipients(valid_numbers, chunk_size=100)

    # 4. Step C: Run through engine.py (Async dispatch)
    dispatch_report = await dispatch_broadcast(chunked_batches=batches, message=message)

    return {
        "status": "Success",
        "csv_filename": file.filename,
        "validation_summary": {
            "total_extracted_from_csv": len(raw_extracted_numbers),
            "total_valid_e164": len(valid_numbers),
            "total_invalid_rejected": len(invalid_numbers),
            "rejected_samples": invalid_numbers[:5],  # Show first 5 rejected
        },
        "dispatch_summary": dispatch_report,
    }