from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    session: AsyncSession = Depends(get_db),
) -> ChatResponse:
    response = await chat_service.chat(
        session=session,
        session_id=request.session_id,
        user_message=request.message,
    )

    return ChatResponse(
        session_id=request.session_id,
        response=response,
    )