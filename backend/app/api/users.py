from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import get_db


router = APIRouter()


@router.post("/users")
def create_user(
    name: str,
    email: str,
    db: Session = Depends(get_db)
):
    user = User(
        name=name,
        email=email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
