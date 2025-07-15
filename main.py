import asyncio
from contextlib import asynccontextmanager

import uvicorn
import logging

from typing import List
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from typing_extensions import Tuple
from fastapi.routing import APIRouter

from api.config.settings import get_settings
from api.config.logger import setup_logging
from api.database.mongo_repository import MongoRepository
from api.v1.routes.health_check_route import health_check_router
from api.v1.routes.reservation_route import reservation_router


setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()


def register_routers(app: FastAPI, version: str) -> None:
    """
    Registers a list of routers to the FastAPI app under the specified API version.

    Args:
        app (FastAPI): The FastAPI application instance.
        version (str): API version string (e.g., 'v1').
        routers (List[Tuple[APIRouter, str]]): List of tuples containing routers and their path prefixes.
    """

    base_path = f"/api/{version}"

    routers = [
        (health_check_router, "health"),
        (reservation_router, "reservation"),
    ]

    for router, tag in routers:

        try:
            app.include_router(router, prefix=f"{base_path}/{tag}", tags=[tag.capitalize()])
            logger.info(f"Registered router at '{base_path}/{tag}'")

        except Exception as e:
            logger.exception(f"Failed to register router '{tag}': {e}")
            raise


async def init_database():
    """
    Initialize Mongo DB instance
    """
    # MongoDB Connection
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongo_db = mongo_client.get_database(settings.MONGO_DB_NAME)

    mongo = MongoRepository(
        client=mongo_client,
        db=mongo_db,
        # collection_name=settings.MONGO_COLLECTION_NAME
    )

    await mongo_client.admin.command("ping")
    logger.info("Connected to MongoDB")

    return mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown lifecycle.

    Args:
        app (FastAPI): FastAPI instance.
    """

    try:
        logger.info("Initializing application...")
        app.state.settings = settings

        while True:
            try:

                app.state.mongo = await init_database()
                break

            except Exception:
                logger.warning("Waiting for MongoDB to be ready...", exc_info=True)
                await asyncio.sleep(2)  # Avoid tight loop

        logger.info("Application initialized successfully")

        url = f"http://{settings.host}:{settings.port}/"
        logger.info(f"🌐 API is running at: {url}")

        yield  # Yield control to the app

    except Exception as e:
        logger.exception("Error during startup initialization")
        raise RuntimeError("Failed to initialize application") from e

    finally:
        logger.info("Shutting down...")
        mongo: AsyncIOMotorClient = app.state.mongo
        mongo.close()
        logger.info("MongoDB connection closed.")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    Returns:
        FastAPI: The configured application.
    """
    try:
        app = FastAPI(
            title="UpStay-API",
            version=settings.app_version,
            lifespan=lifespan
        )

        register_routers(app, settings.app_version)
        logger.info("FastAPI application created successfully")
        return app

    except Exception as e:
        logger.exception("Failed to create FastAPI application")
        raise


app = create_app()

if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers,
            log_level=settings.log_level,
            reload=settings.reload,
        )
    except Exception as e:
        logger.exception("Failed to start the Uvicorn server")
