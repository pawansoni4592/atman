from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Memory, User
from ..schemas import MemoryCreate, MemoryResponse

router = APIRouter(prefix="/api/v1/memories", tags=["memories"])


@router.post("", response_model=MemoryResponse, status_code=201)
def create_memory(payload: MemoryCreate, db: Session = Depends(get_db)) -> Memory:
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    memory = Memory(
        user_id=payload.user_id,
        content=payload.content,
        memory_type=payload.memory_type,
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory


@router.get("", response_model=list[MemoryResponse])
def list_memories(user_id: str, db: Session = Depends(get_db)) -> list[Memory]:
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return list(
        db.scalars(
            select(Memory)
            .where(Memory.user_id == user_id)
            .order_by(Memory.created_at.desc())
        )
    )
