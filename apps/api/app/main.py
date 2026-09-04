from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from .db import get_db
from .routes import chat, conversations, memories, users

app = FastAPI(
    title="Atman API",
    description="Backend API for the Atman personal AI mentor.",
    version="0.1.0",
)

app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(memories.router)
app.include_router(chat.router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "atman-api"}


@app.get("/health/database", tags=["system"])
def database_health(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok", "service": "atman-postgres"}
