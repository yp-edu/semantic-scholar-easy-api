"""
Recommendations router.
"""

from loguru import logger
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional

from .schema import (
    PaperRecommendationsRequest,
    RecommendedPaper,
    PaperRecommendationsResponse,
)

router = APIRouter()


# Mock data retrieval function
def get_recommended_papers(positive_paper_ids, negative_paper_ids, limit, fields):
    logger.info(
        f"Retrieving recommended papers with positive_paper_ids={positive_paper_ids}, negative_paper_ids={negative_paper_ids}, limit={limit}, fields={fields}"
    )
    # This is a mock function that should be replaced by actual logic
    # for retrieving recommendations, for example from a machine learning model or database.
    return [
        {
            "paperId": "12345",
            "title": "Recommended Paper 1",
            "url": "http://example.com/1",
            "authors": ["Author A", "Author B"],
        },
        {
            "paperId": "67890",
            "title": "Recommended Paper 2",
            "url": "http://example.com/2",
            "authors": ["Author C", "Author D"],
        },
    ][:limit]


@router.post("/papers/", response_model=PaperRecommendationsResponse)
async def get_paper_recommendations(
    request: PaperRecommendationsRequest,
    limit: int = Query(
        100, le=500, description="How many recommendations to return. Maximum 500."
    ),
    fields: Optional[str] = Query(
        None,
        description="Comma-separated list of fields to return (e.g., title, url, authors)",
    ),
):
    logger.info(
        f"Received POST request for paper recommendations with positivePaperIds={request.positivePaperIds}, negativePaperIds={request.negativePaperIds}, limit={limit}, fields={fields}"
    )

    # Validate input
    if not request.positivePaperIds:
        logger.error("positivePaperIds must not be empty")
        raise HTTPException(
            status_code=400, detail="positivePaperIds must not be empty"
        )

    # Retrieve recommended papers
    recommended_papers_data = get_recommended_papers(
        request.positivePaperIds, request.negativePaperIds, limit, fields
    )
    recommended_papers = [
        RecommendedPaper(**paper) for paper in recommended_papers_data
    ]

    logger.info(f"Returning {len(recommended_papers)} recommended papers")
    return PaperRecommendationsResponse(recommendedPapers=recommended_papers)


@router.get("/papers/{paper_id}", response_model=PaperRecommendationsResponse)
async def get_single_paper_recommendations(
    paper_id: str = Path(
        ..., description="The ID of the paper to get recommendations for."
    ),
    from_pool: str = Query(
        "recent",
        regex="^(recent|all-cs)$",
        description="Which pool of papers to recommend from.",
    ),
    limit: int = Query(
        100, le=500, description="How many recommendations to return. Maximum 500."
    ),
    fields: Optional[str] = Query(
        None,
        description="Comma-separated list of fields to return (e.g., title, url, authors)",
    ),
):
    logger.info(
        f"Received GET request for paper recommendations with paper_id={paper_id}, from_pool={from_pool}, limit={limit}, fields={fields}"
    )

    # Retrieve recommended papers
    recommended_papers_data = get_recommended_papers([paper_id], [], limit, fields)
    recommended_papers = [
        RecommendedPaper(**paper) for paper in recommended_papers_data
    ]

    logger.info(
        f"Returning {len(recommended_papers)} recommended papers for paper_id={paper_id}"
    )
    return PaperRecommendationsResponse(recommendedPapers=recommended_papers)
