from fastapi import APIRouter, HTTPException
from models.api_models import (
    ChatInitRequest,
    ChatInitResponse,
    ChatMessageRequest,
    ChatMessageResponse
)
from services.rag_service import initialize_vector_store, get_answer

router = APIRouter()


@router.post("/initialize", response_model=ChatInitResponse)
async def initialize_chat(request: ChatInitRequest):
    try:
        session_id = initialize_vector_store(request.documentation)
        return ChatInitResponse(sessionId=session_id, status="ready")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize chat: {str(e)}")


@router.post("/message", response_model=ChatMessageResponse)
async def chat_message(request: ChatMessageRequest):
    try:
        result = get_answer(
            request.sessionId,
            request.message,
            request.history
        )

        return ChatMessageResponse(
            response=result["response"],
            sources=result["sources"]
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
