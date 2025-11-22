from ..schemas.chatbot import ChatRequest, ChatResponse
from ..database import get_async_session, Chat
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import os
from openai import OpenAI

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

class ChatbotService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_response(self, request: ChatRequest) -> ChatResponse:
        # Save user message
        user_chat = Chat(message=request.message, sender="user")
        self.session.add(user_chat)
        await self.session.commit()
        # Get last 10 messages (including the new user message)
        result = await self.session.execute(select(Chat).order_by(Chat.createdAt.desc()).limit(10))
        history = list(reversed(result.scalars().all()))
        # Format history for OpenRouter
        openai_messages = [
            {"role": "user" if m.sender == "user" else "assistant", "content": m.message}
            for m in history
        ]
        # Add the current user message if not already present (should be present)
        # Call OpenRouter (OpenAI-compatible) to get answer
        completion = client.chat.completions.create(
            extra_headers={},
            model="openai/gpt-4o",
            messages=openai_messages
        )
        answer = completion.choices[0].message.content
        # Save bot reply
        bot_chat = Chat(message=answer, sender="bot")
        self.session.add(bot_chat)
        await self.session.commit()
        # Get last 10 messages again for response history
        result = await self.session.execute(select(Chat).order_by(Chat.createdAt.desc()).limit(10))
        history = list(reversed(result.scalars().all()))
        response = ChatResponse(answer=answer)
        response.history = [
            {"message": m.message, "sender": m.sender, "createdAt": m.createdAt.isoformat()} for m in history
        ]
        return response 