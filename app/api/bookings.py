from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import booking_service

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(
    booking_data: BookingCreate,
    session: AsyncSession = Depends(get_db),
) -> BookingResponse:

    booking = await booking_service.create_booking(
        session=session,
        booking_data=booking_data,
    )

    return BookingResponse.model_validate(booking)

@router.get(
    "/",
    response_model=list[BookingResponse],
)
async def get_bookings(
    session: AsyncSession = Depends(get_db),
) -> list[BookingResponse]:

    bookings = await booking_service.get_all_bookings(
        session=session,
    )

    return [
        BookingResponse.model_validate(booking)
        for booking in bookings
    ]

@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
async def get_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db),
) -> BookingResponse:

    booking = await booking_service.get_booking_by_id(
        session=session,
        booking_id=booking_id,
    )

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    return BookingResponse.model_validate(booking)