"""NVIDIA Kimi K2.6 chat proxy with streaming support.

Thin controller: delegates to ChatService for streaming logic.
"""

import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter()

# Singleton — no DB dependency, just NVIDIA API proxy
_chat_service = ChatService()


@router.post("")
async def chat(request: ChatRequest) -> StreamingResponse:
    """Stream a chat completion from NVIDIA Kimi K2.6.

    Accepts user message + optional conversation history.
    Returns Server-Sent Events with incremental content chunks.
    """
    messages: list[dict[str, str]] = [
        {"role": msg.role, "content": msg.content} for msg in request.history
    ]
    messages.append({"role": "user", "content": request.message})

    return StreamingResponse(
        _chat_service.stream_completion(messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
