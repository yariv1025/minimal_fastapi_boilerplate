import logging
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
health_check_router = APIRouter()


@health_check_router.get("/", tags=["Health"])
def root():
    """
    Health check endpoint to verify the service is running.
    """
    try:
        logger.info("GET / - Health check requested")
        return {"status": "OK"}

    except Exception as e:
        logger.exception("Health check failed")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Health check failed") from e
