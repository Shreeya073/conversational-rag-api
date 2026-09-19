from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.schemas.booking import BookingCreate

class BookingRepository:

    async def create(
        self,
        session: AsyncSession,
        booking_data: BookingCreate,
    ) -> Booking:

        booking = Booking(
            name=booking_data.name,
            email=booking_data.email,
            date=booking_data.date,
            time=booking_data.time,
        )

        session.add(booking)

        await session.commit()
        await session.refresh(booking)

        return booking

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[Booking]:

        result = await session.execute(
            select(Booking).order_by(Booking.id.desc())
        )

        return list(result.scalars().all())

    async def get_by_id(
        self,
        session: AsyncSession,
        booking_id: int,
    ) -> Booking | None:

        result = await session.execute(
            select(Booking).where(Booking.id == booking_id)
        )

        return result.scalar_one_or_none()

booking_repository = BookingRepository()