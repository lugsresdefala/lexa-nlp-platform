from fastapi import Request

async def get_client_id(request: Request) -> str:
    """Return a unique identifier for the request's client."""
    client = request.client
    return client.host if client else "unknown"
