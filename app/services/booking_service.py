from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.repositories.booking_repository import booking_repository
from app.schemas.booking import BookingCreate

class BookingService:

    async def create_booking(
        self,
        session: AsyncSession,
        booking_data: BookingCreate,
    ) -> Booking:

        return await booking_repository.create(
            session=session,
            booking_data=booking_data,
        )

    async def get_all_bookings(
        self,
        session: AsyncSession,
    ) -> list[Booking]:

        return await booking_repository.get_all(
            session=session,
        )

    async def get_booking_by_id(
        self,
        session: AsyncSession,
        booking_id: int,
    ) -> Booking | None:

        return await booking_repository.get_by_id(
            session=session,
            booking_id=booking_id,
        )

booking_service = BookingService()