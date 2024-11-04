"""
Global API Schema
"""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    error: str


class SuccessDetail(BaseModel):
    success: str
