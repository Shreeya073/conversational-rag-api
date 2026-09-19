from typing import Any

import httpx

from app.core.config import settings
from app.schemas.booking_extraction import BookingExtraction

class LLMService:

    async def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:

        payload: dict[str, Any] = {
            "model": settings.ollama_model,
            "messages": messages,
            "stream": False,
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.ollama_url}/api/chat",
                json=payload,
            )

            response.raise_for_status()

            data: dict[str, Any] = response.json()

        message = data.get("message")

        if not isinstance(message, dict):
            raise ValueError("Invalid response received from Ollama.")

        content = message.get("content")

        if not content:
            raise ValueError("Ollama returned an empty response.")

        return str(content)

    async def extract_booking(
        self,
        messages: list[dict[str, str]],
    ) -> BookingExtraction:

        extraction_messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "Extract interview booking information ONLY from "
                    "information explicitly provided by the user.\n\n"

                    "NEVER guess, infer, invent, or assume a value.\n"
                    "NEVER create a value just because the conversation "
                    "is about booking an interview.\n\n"

                    "If the user has not explicitly provided a value, "
                    "you MUST return null for that field.\n\n"

                    "Return ONLY valid JSON with these fields:\n"
                    "{"
                    '"name": string or null, '
                    '"email": string or null, '
                    '"date": "YYYY-MM-DD" or null, '
                    '"time": "HH:MM:SS" or null'
                    "}\n\n"
                ),
            },
            *messages,
        ]

        payload: dict[str, Any] = {
            "model": settings.ollama_model,
            "messages": extraction_messages,
            "stream": False,
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.ollama_url}/api/chat",
                json=payload,
            )

            response.raise_for_status()

            data: dict[str, Any] = response.json()

        message = data.get("message")

        if not isinstance(message, dict):
            raise ValueError("Invalid extraction response.")

        content = message.get("content")

        if not isinstance(content, str):
            raise ValueError("Invalid extraction content.")

        return BookingExtraction.model_validate_json(content)

llm_service = LLMService()