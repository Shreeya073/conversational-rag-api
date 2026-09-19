from fastapi import FastAPI

from app.api.bookings import router as bookings_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="Conversational RAG API",
    version="1.0.0",
    description="Conversational RAG API with booking interview.",
)

app.include_router(bookings_router)
app.include_router(chat_router)

@app.get("/", tags=["Status"])
async def root() -> dict[str, str]:
    return {
        "message": "Conversational RAG API is running"
    }