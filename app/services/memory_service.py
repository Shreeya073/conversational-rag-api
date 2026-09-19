import json

from redis.asyncio import Redis
from app.core.config import settings

class MemoryService:

    def __init__(self) -> None:
        self.redis: Redis = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    def _get_key(self, session_id: str) -> str:

        return f"chat:memory:{session_id}"

    def _get_booking_key(self, session_id: str) -> str:

        return f"chat:booking:{session_id}"

    def _get_booking_started_key(self, session_id: str) -> str:

        return f"chat:booking-started:{session_id}"

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:

        key = self._get_key(session_id)

        message = {
            "role": role,
            "content": content,
        }

        await self.redis.rpush(
            key,
            json.dumps(message),
        )

    async def get_messages(
        self,
        session_id: str,
    ) -> list[dict[str, str]]:

        key = self._get_key(session_id)

        messages = await self.redis.lrange(
            key,
            0,
            -1,
        )

        return [
            json.loads(message)
            for message in messages
        ]

    async def clear_memory(
        self,
        session_id: str,
    ) -> None:

        await self.redis.delete(
            self._get_key(session_id),
            self._get_booking_key(session_id),
            self._get_booking_started_key(session_id),
        )

    async def set_booking_started(
        self,
        session_id: str,
    ) -> None:

        key = self._get_booking_started_key(session_id)

        await self.redis.set(
            key,
            "1",
        )

    async def is_booking_started(
        self,
        session_id: str,
    ) -> bool:

        key = self._get_booking_started_key(session_id)

        value = await self.redis.get(key)

        return value == "1"

    async def set_booking_id(
        self,
        session_id: str,
        booking_id: int,
    ) -> None:

        key = self._get_booking_key(session_id)

        await self.redis.set(
            key,
            str(booking_id),
        )

    async def get_booking_id(
        self,
        session_id: str,
    ) -> int | None:

        key = self._get_booking_key(session_id)

        value = await self.redis.get(key)

        if value is None:
            return None

        return int(value)

    async def close(self) -> None:

        await self.redis.aclose()

memory_service = MemoryService()