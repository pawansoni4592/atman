from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Conversation, Message, User
from ..schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    conversation = db.get(Conversation, payload.conversation_id) if payload.conversation_id else None
    if conversation is None:
        conversation = Conversation(user_id=payload.user_id)
        db.add(conversation)
        db.flush()
    elif conversation.user_id != payload.user_id:
        raise HTTPException(status_code=403, detail="Conversation does not belong to user")

    user_message = Message(conversation_id=conversation.id, role="user", content=payload.message)
    db.add(user_message)
    db.flush()

    assistant_text = (
        "I received your message. The persistent conversation layer is working, "
        "and the AI response provider will be connected next."
    )
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=assistant_text,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(conversation)
    db.refresh(user_message)
    db.refresh(assistant_message)

    return ChatResponse(
        conversation=conversation,
        user_message=user_message,
        assistant_message=assistant_message,
    )
