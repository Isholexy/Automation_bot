# Async Bulk SMS Broadcasting Engine 🚀

A modular, high-performance asynchronous bulk SMS dispatching system built with modern Python . The application processes recipient lists via CSV, cleans and normalizes numbers to international E.164 formats, chunks contact batches, and dispatches SMS payloads concurrently using non-blocking HTTP connection pools.

## Key Features

* **Asynchronous Concurrency:** Powered by `asyncio` and `httpx` with HTTP connection pooling for maximum throughput.
* **E.164 Validation:** Integrates Google's `phonenumbers` library to strip invalid entries and format regional numbers reliably.
* **Batch Slicing:** Automatically chunks large contact lists into configurable batch sizes (default: 100 recipients) to meet provider payload limits.
* **REST API Interface:** Built with FastAPI, providing automated interactive OpenAPI/Swagger documentation (`/docs`) for CSV file uploads.
* **Provider Agnostic:** Modular design allowing quick adaptation between regional gateways (e.g., Termii) and global providers (e.g., Twilio, Plivo).

---

## Architecture Overview

```text
[ CSV Upload / Input ]
          │
          ▼
    validator.py       ──► Validates digits & converts to E.164 format (+234...)
          │
          ▼
     chunker.py        ──► Slices clean lists into sub-batches of N items
          │
          ▼
      engine.py        ──► Non-blocking concurrent async HTTP execution via httpx


## Quickstart Guide

1. Requirements
Python 3.12+

FastAPI & Uvicorn

HTTPX

Phonenumbers

2. Installation & Setup
Clone the repository and install the dependencies:

Bash
git clone [https://github.com/Isholexy/Automation_bot](https://github.com/Isholexy/Automation_bot)
cd Automation_bot

python -m pip install fastapi uvicorn httpx phonenumbers python-multipart

3. Run the API Server
Start the ASGI server using Uvicorn:

Bash
python -m uvicorn main:app --reload


4. Test via Interactive Docs
Open your browser and navigate to http://127.0.0.1:8000/docs.

Expand the POST /broadcast/csv endpoint and click Try it out.

Upload a CSV file containing recipient phone numbers in Column A, enter your broadcast message, and click Execute.

⚙️ Environment Variables
For production use, configure your SMS gateway credentials in a .env file or directly in your environment:

Code snippet
API_KEY=your_api_key_here
SENDER_ID=your_registered_sender_id



📄 License
Distributed under the MIT License. See LICENSE for more information.