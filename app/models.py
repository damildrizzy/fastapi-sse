from sqlalchemy import Column, String, Integer
from .database import Base


class Cookie(Base):
    id = Column(Integer, primary_key=True)
    message = Column(String)

