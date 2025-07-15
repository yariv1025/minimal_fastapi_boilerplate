import datetime
import logging
from http import HTTPStatus

from uuid import UUID, uuid4
from typing import Dict, List
from starlette.exceptions import HTTPException
from datetime import datetime, UTC, timedelta, time

from api.config.settings import get_settings
from api.database.mongo_repository import MongoRepository
from api.models.reservation_model import ReservationResponse, ReservationCreate

settings = get_settings()
logger = logging.getLogger(__name__)

COLLECTION = "reservations"

INVENTORY = {
        "A": 261,
        "B": 137,
        "C": 130,
        "D": 58,
        "E": 4
    }


async def make_reservation(mongo: MongoRepository, reservation_details: Dict) -> ReservationResponse:
    # Validate input with Pydantic
    data = ReservationCreate(**reservation_details)

    reservation_id = uuid4()
    now = datetime.now(UTC)

    document = {
        "reservation_id": str(reservation_id),
        "customer_name": data.customer_name,
        "guest_name": data.guest_name,
        "room_type": data.room_type,
        "room_id": data.room_id,
        "hotel_id": data.hotel_id,
        "arrival_date": data.arrival_date.isoformat(),
        "nights": data.nights,
        "room_count": data.room_count,
        "created_at": now.isoformat()
    }
    result = await mongo.create(data=document, collection=COLLECTION)

    return ReservationResponse(**result)


async def get_reservation_by_uuid(mongo: MongoRepository, uuid: UUID) -> ReservationResponse:
    """"""
    reservation = await mongo.get_by_id(data={"reservation_id": str(uuid)}, collection=COLLECTION)

    if not reservation:
        logger.warning(f"Reservation not found: {uuid}")
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Reservation with UUID {uuid} not found."
        )

    try:
        return ReservationResponse(**reservation)
    except Exception as e:
        logger.exception(f"Failed to parse reservation document: {reservation}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to parse reservation data from database."
        )


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def add_occupancy(room_id, start, end, count, occupancy_calendar) -> None:
    """
    Updates the occupancy calendar for a given room type,
    incrementing the count of occupied rooms for every day in the specified date range.
    Returns: None

    """
    for single_date in daterange(start.date(), end.date()):
        occupancy_calendar[room_id][single_date] = occupancy_calendar[room_id].get(single_date, 0) + count


def populate_overlapping_target(reservations_content: List, target_checkin: datetime, target_checkout: datetime, occupancy_calendar: Dict) -> None:
    """
    Populate occupancy calendar only for reservations overlapping target period
    Returns: None

    """
    for row in reservations_content:
        res = ReservationResponse(**row)

        checkin_time = datetime.combine(res.arrival_date, time(hour=10, minute=0, second=0))
        checkout_date = res.arrival_date + timedelta(days=res.nights)
        checkout_time = datetime.combine(checkout_date, time(hour=14, minute=0, second=0))

        if not (checkout_time <= target_checkin or checkin_time >= target_checkout):
            add_occupancy(res.room_id, checkin_time, checkout_time, res.room_count, occupancy_calendar)


def calculate_availability(target_checkin: datetime, target_checkout: datetime, occupancy_calendar: Dict) -> Dict:
    """
    Calculate availability
    Returns: minimum availability over target period per room type

    """
    availability = {}

    for room_type, total in INVENTORY.items():
        min_available = total
        for single_date in daterange(target_checkin.date(), target_checkout.date()):
            occupied = occupancy_calendar[room_type].get(single_date, 0)
            available = total - occupied
            if available < min_available:
                min_available = available
        if min_available < 0:
            raise HTTPException(
                status_code=409,
                detail=f"Overbooking detected for room type '{room_type}' during the reservation period."
            )
        availability[room_type] = min_available

    logger.info(f"Availability result: {availability}")
    return availability


async def get_availability(mongo: MongoRepository, uuid: UUID) -> Dict:
    """"""

    reservations = await mongo.get_all(collection=COLLECTION)

    target = None

    for res in reservations:
        if res.get("reservation_id") == str(uuid):
            target = ReservationResponse(**res)
            break

    if not target:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Reservation #{uuid} not found."
        )

    # Occupancy calendar: room_type | date | count
    occupancy_calendar = {room_type: {} for room_type in INVENTORY.keys()}

    checkin_time = datetime.combine(target.arrival_date, time(hour=10, minute=0, second=0))
    checkout_date = target.arrival_date + timedelta(days=target.nights)
    checkout_time = datetime.combine(checkout_date, time(hour=14, minute=0, second=0))

    populate_overlapping_target(reservations, checkin_time, checkout_time, occupancy_calendar)

    return {
        "available": calculate_availability(checkin_time, checkout_time, occupancy_calendar)
    }


async def delete_reservation(mongo: MongoRepository, uuid: UUID) -> Dict:
    """"""
    filter = {"reservation_id": str(uuid)}
    deleted_count = await mongo.delete(data=filter, collection=COLLECTION)

    if deleted_count == 0:
        logger.warning(f"Reservation not found for deletion: {uuid}")
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Reservation with UUID {uuid} not found."
        )

    logger.info(f"Reservation {uuid} deleted successfully.")
    return {"message": f"Reservation {uuid} deleted successfully."}