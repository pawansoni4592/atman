import os
from collections.abc import Sequence

from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Memory

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_text(text: str) -> list[float]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model=os.getenv("ATMAN_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        input=text,
    )
    return response.data[0].embedding


def create_memory(
    db: Session,
    *,
    user_id: str,
    content: str,
    memory_type: str = "fact",
) -> Memory:
    memory = Memory(
        user_id=user_id,
        content=content,
        memory_type=memory_type,
        embedding=embed_text(content),
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory


def search_memories(
    db: Session,
    *,
    user_id: str,
    query: str,
    limit: int = 5,
) -> Sequence[Memory]:
    query_embedding = embed_text(query)
    distance = Memory.embedding.cosine_distance(query_embedding)
    statement = (
        select(Memory)
        .where(Memory.user_id == user_id, Memory.embedding.is_not(None))
        .order_by(distance.asc())
        .limit(limit)
    )
    return list(db.scalars(statement))
