"""
Recommendations schema.
"""

from pydantic import BaseModel
from typing import List, Optional


class PaperRecommendationsRequest(BaseModel):
    positivePaperIds: List[str]
    negativePaperIds: Optional[List[str]] = []


class RecommendedPaper(BaseModel):
    paperId: str
    title: Optional[str] = None
    url: Optional[str] = None
    authors: Optional[List[str]] = None


class PaperRecommendationsResponse(BaseModel):
    recommendedPapers: List[RecommendedPaper]
