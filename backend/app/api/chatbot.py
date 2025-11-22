from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.chatbot_service import ChatbotService
from ..schemas.chatbot import ChatRequest, ChatResponse
from ..database import get_async_session
from ..services.db_chat import init_database, get_response_with_db_history

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/ask", response_model=ChatResponse)
async def ask_chatbot(
    request: ChatRequest,
    session: AsyncSession = Depends(get_async_session)
):
    service = ChatbotService(session)
    return await service.get_response(request)

@router.post("/db-ask")
async def db_ask_chatbot(
    request: ChatRequest,
    session: AsyncSession = Depends(get_async_session)
):
    db = init_database()
    answer = await get_response_with_db_history(request.message, db, session)
    return {"answer": answer} 