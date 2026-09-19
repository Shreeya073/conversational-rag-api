import asyncio
import uuid
import httpx

API_URL = "http://127.0.0.1:8000/chat/"

async def main() -> None:

    session_id = f"terminal-{uuid.uuid4().hex[:8]}"

    print("Interview Booking Assistant")
    print("Type 'exit' to quit.")
    print("-" * 40)

    async with httpx.AsyncClient(timeout=180.0) as client:
        while True:
            user_message = input("You: ").strip()

            if user_message.lower() == "exit":
                print("Goodbye!")
                break

            if not user_message:
                continue

            try:
                response = await client.post(
                    API_URL,
                    json={
                        "session_id": session_id,
                        "message": user_message,
                    },
                )

                response.raise_for_status()

                data = response.json()

                print(f"Assistant: {data['response']}")

            except httpx.HTTPError as error:
                print(f"Request failed: {type(error).__name__}: {error}")

if __name__ == "__main__":
    asyncio.run(main())