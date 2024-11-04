"""
Authentication module for API
"""

from fastapi import HTTPException, Security
from fastapi.security import api_key

from api import constants

api_key_header = api_key.APIKeyHeader(name="X-API-KEY")


async def validate_api_key(key: str = Security(api_key_header)):
    if constants.X_API_KEY == "":
        raise HTTPException(status_code=500, detail="API Key is not set in the server")
    if key != constants.X_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized - API Key is wrong")
    return None
