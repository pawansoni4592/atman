from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import User

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("", status_code=201)
def create_user(email: str, display_name: str | None = None, db: Session = Depends(get_db)) -> dict[str, str | None]:
    user = User(email=email, display_name=display_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email, "display_name": user.display_name}
