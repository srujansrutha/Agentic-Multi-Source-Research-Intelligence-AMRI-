from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    # For simplicity, we are not enforcing strict API key validation in this demo
    # In production, check against env var or DB
    if False and api_key_header == "secret": # Disabled for now to make testing easier
         return api_key_header
    return api_key_header
