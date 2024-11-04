"""
Main API module.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api.library.router as library_router
import api.recommendations.router as recommendations_router
from api import auth, constants
from api.schema import SuccessDetail


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger("uvicorn")
    logger.info(f"Semantic Scholar Easy API {constants.VERSION}: Starting up...")
    yield
    logger.info(f"Semantic Scholar Easy API {constants.VERSION}: Shutting down...")


app = FastAPI(
    title="Semantic Scholar Easy API",
    version=constants.VERSION,
    lifespan=lifespan,
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    summary="Home page",
    tags=["GENERAL"],
    status_code=200,
    response_model=SuccessDetail,
)
async def home():
    """
    Home page.
    """
    return {"success": "Welcome to Semantic Scholar Easy API!"}


@app.get(
    "/healthz",
    summary="Health check",
    tags=["GENERAL"],
    status_code=200,
    response_model=SuccessDetail,
)
async def healthz():
    """
    Health check.
    """
    return {"success": "Healthy!"}


app.include_router(
    library_router.router,
    prefix="/library",
    tags=["LIBRARY"],
    dependencies=[Depends(auth.validate_api_key)],
)

app.include_router(
    recommendations_router.router,
    prefix="/recommendations",
    tags=["RECOMMENDATIONS"],
    dependencies=[Depends(auth.validate_api_key)],
)
