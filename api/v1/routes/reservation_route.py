import logging
from http import HTTPStatus

from uuid import UUID
from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.controller import reservation_controller
from api.models.reservation_model import ReservationResponse

logger = logging.getLogger(__name__)

reservation_router = APIRouter(
    tags=["Reservation"]
)


@reservation_router.post("/make", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def make_reservation(request: Request):
    """
    Create a reservation.
    """
    mongo = request.app.state.mongo
    reservation_details = await request.json()
    result = await reservation_controller.make_reservation(mongo, reservation_details)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=HTTPStatus.CREATED)


@reservation_router.get("/{reservation_uuid}")
async def get_my_reservation(request: Request, reservation_uuid: UUID):
    """
    Get reservation data by UUID.
    """
    mongo = request.app.state.mongo
    result = await reservation_controller.get_reservation_by_uuid(mongo, reservation_uuid)
    return JSONResponse(content=result.model_dump(mode="json"))


@reservation_router.get("/room_availability/{reservation_uuid}")
async def get_reservation_availability(request: Request, reservation_uuid: UUID):
    """
    Get room availability based on reservation UUID.
    """
    mongo = request.app.state.mongo
    result = await reservation_controller.get_availability(mongo, reservation_uuid)
    return JSONResponse(content=result)


@reservation_router.delete("/{reservation_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(request: Request, reservation_uuid: UUID):
    """
    Delete reservation by UUID.
    """
    mongo = request.app.state.mongo
    res = await reservation_controller.delete_reservation(mongo, reservation_uuid)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=res)
