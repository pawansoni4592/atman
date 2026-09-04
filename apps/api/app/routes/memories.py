from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Memory, User
from ..schemas import MemoryCreate, MemoryResponse
from ..services.memory import create_memory, search_memories

router = APIRouter(prefix="/api/v1/memories", tags=["memories"])


@router.post("", response_model=MemoryResponse, status_code=201)
def create_memory_endpoint(payload: MemoryCreate, db: Session = Depends(get_db)) -> Memory:
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        return create_memory(
            db,
            user_id=payload.user_id,
            content=payload.content,
            memory_type=payload.memory_type,
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=502, detail="Memory embedding provider is unavailable") from exc


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


@router.get("/search", response_model=list[MemoryResponse])
def semantic_memory_search(
    user_id: str,
    query: str,
    limit: int = 5,
    db: Session = Depends(get_db),
) -> list[Memory]:
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")
    if not 1 <= limit <= 20:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 20")
    try:
        return list(search_memories(db, user_id=user_id, query=query, limit=limit))
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Memory embedding provider is unavailable") from exc
