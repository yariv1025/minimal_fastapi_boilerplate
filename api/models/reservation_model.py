from uuid import UUID
from datetime import date
from pydantic import BaseModel, Field


# class Reservation(BaseModel):
#     reservation_id: UUID = Field(alias="reservation_id")
#     room_id: str
#     hotel_id: int
#     guest_name: str
#     arrival_date: datetime
#     nights: int
#     room_count: int
#
#
#     @field_validator("arrival_date", mode="before")
#     @classmethod
#     def fix_datetime(cls, v):
#         if isinstance(v, str):
#             return datetime.fromisoformat(v.replace(" ", "T"))
#         return v


class ReservationCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    room_type: str = Field(..., min_length=1)
    arrival_date: date
    guest_name: str = Field(..., min_length=1)
    hotel_id: int = Field(..., ge=1)
    room_id: str = Field(..., pattern="^(A|B|C|D)$")
    nights: int = Field(..., ge=1)
    room_count: int = Field(..., ge=1)


class ReservationResponse(BaseModel):
    reservation_id: UUID
    guest_name: str
    room_id: str
    room_type: str
    hotel_id: int
    arrival_date: date
    nights: int
    room_count: int
    _id: str