import asyncio
import os

import httpx

# Load environment variables for security (never hardcode credentials)
API_KEY = os.getenv("SMS_API_KEY", "your_api_key_here")
BASE_URL = os.getenv("SMS_BASE_URL", "https://api.ng.termii.com")
SENDER_ID = os.getenv("SMS_SENDER_ID", "N-Alert")


async def send_single_batch(
    client: httpx.AsyncClient, 
    batch: list[str], 
    message: str
) -> dict:
    """
    Sends a single chunk of up to 100 phone numbers to the SMS Gateway API.
    Returns the gateway response or captures network errors cleanly.
    """
    url = f"{BASE_URL}/api/sms/send/bulk"
    
    payload = {
        "to": batch,
        "from": SENDER_ID,
        "sms": message,
        "type": "plain",
        "channel": "generic",
        "api_key": API_KEY,
    }

    try:
        # Set an explicit timeout to prevent hanging connections
        response = await client.post(url, json=payload, timeout=10.0)
        
        return {
            "status_code": response.status_code,
            "count": len(batch),
            "data": response.json() if response.headers.get("content-type") == "application/json" else response.text,
        }
    except httpx.HTTPError as exc:
        return {
            "status_code": 500,
            "count": len(batch),
            "error": f"HTTP Error during dispatch: {str(exc)}",
        }


async def dispatch_broadcast(
    chunked_batches: list[list[str]], 
    message: str
) -> dict:
    """
    Manages concurrent dispatch across all batch chunks using httpx connection pooling.
    """
    # Use AsyncClient with custom connection limits to avoid overloading sockets
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
    
    async with httpx.AsyncClient(limits=limits) as client:
        # Create asynchronous tasks for all batches
        tasks = [
            send_single_batch(client, batch, message) 
            for batch in chunked_batches
        ]
        
        # Execute all HTTP requests concurrently
        results = await asyncio.gather(*tasks)

    # Aggregate performance metrics
    total_dispatched = sum(res["count"] for res in results)
    successful_batches = sum(1 for res in results if res["status_code"] == 200)

    return {
        "total_recipients": total_dispatched,
        "total_batches": len(chunked_batches),
        "successful_batches": successful_batches,
        "failed_batches": len(chunked_batches) - successful_batches,
        "batch_details": results,
    }