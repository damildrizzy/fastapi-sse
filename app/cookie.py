from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/", response_model=schemas.Cookie)
def get_latest_cookie(
    cookie: schemas.Cookie, db: Session = Depends(get_db)
) -> models.Cookie:
    cookies = db.query(models.Cookie).filter(opened=False).last()
    return cookies


@router.post("/create", response_model=schemas.Cookie)
def create_cookie(
    cookie: schemas.CookieCreate, db: Session = Depends(get_db)
) -> models.Cookie:
    cookie = models.Cookie(message=cookie.message)
    db.add(cookie)
    db.commit()
    db.refresh(cookie)
    return cookie
