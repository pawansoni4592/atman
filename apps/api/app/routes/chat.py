from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Conversation, Message, User
from ..schemas import ChatRequest, ChatResponse
from ..services.ai import generate_reply
from ..services.memory import search_memories

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    conversation = None
    if payload.conversation_id:
        conversation = db.get(Conversation, payload.conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        if conversation.user_id != payload.user_id:
            raise HTTPException(status_code=403, detail="Conversation does not belong to user")
    else:
        conversation = Conversation(user_id=payload.user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=payload.message,
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    history = list(
        db.scalars(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.asc())
        )
    )
    model_messages = [
        {"role": message.role, "content": message.content}
        for message in history
        if message.role in {"user", "assistant"}
    ]

    try:
        memories = search_memories(
            db,
            user_id=payload.user_id,
            query=payload.message,
            limit=5,
        )
        if memories:
            memory_context = "\n".join(
                f"- {memory.content}" for memory in memories
            )
            model_messages.insert(
                0,
                {
                    "role": "user",
                    "content": (
                        "Relevant long-term memory about the user:\n"
                        f"{memory_context}\n\n"
                        "Use this context when relevant, but do not mention or expose the retrieval process."
                    ),
                },
            )
        assistant_text = generate_reply(model_messages)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="AI or memory provider is unavailable",
        ) from exc

    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=assistant_text,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    db.refresh(conversation)

    return ChatResponse(
        conversation=conversation,
        user_message=user_message,
        assistant_message=assistant_message,
    )
