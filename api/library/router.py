from loguru import logger
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

library_router = APIRouter()


# Define response models
class ScrapedPaper(BaseModel):
    paperId: str
    title: Optional[str] = None
    url: Optional[str] = None
    authors: Optional[List[str]] = None


# Scrape library function
def scrape_library(url):
    papers = []
    while url:
        logger.info(f"Scraping URL: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Ensure we get a successful response
        soup = BeautifulSoup(response.text, "html.parser")

        # Find papers using the specified CSS selector (to be filled by user)
        paper_elements = soup.select("YOUR_CSS_SELECTOR_HERE")
        for element in paper_elements:
            # Extract information from the element (e.g., title, URL, authors)
            paper = {
                "paperId": element.get("data-paper-id", "unknown"),
                "title": element.get_text(strip=True),
                "url": element.get("href"),
                "authors": [],  # Adjust as needed to extract author information
            }
            papers.append(paper)

        # Check if there is a next page
        next_page = soup.select_one("YOUR_NEXT_PAGE_SELECTOR_HERE")
        if next_page and next_page.get("href"):
            # Update URL for the next page
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            page_param = query_params.get("page", [1])[0]
            new_page_number = int(page_param) + 1
            query_params["page"] = [new_page_number]
            new_query = urlencode(query_params, doseq=True)
            url = urlunparse(parsed_url._replace(query=new_query))
        else:
            url = None

    return papers


@library_router.get("/library/", response_model=List[ScrapedPaper])
async def scrape_library_endpoint(
    url: str = Query(..., description="The URL of the library page to scrape."),
):
    logger.info(f"Received GET request to scrape library with URL={url}")

    # Scrape the library URL
    scraped_papers = scrape_library(url)
    scraped_paper_models = [ScrapedPaper(**paper) for paper in scraped_papers]

    logger.info(
        f"Returning {len(scraped_paper_models)} scraped papers from the library"
    )
    return scraped_paper_models
