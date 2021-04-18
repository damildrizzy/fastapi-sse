from fastapi import FastAPI
from app import cookie, models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(cookie.router, prefix="/cookie", tags=["cookie"])