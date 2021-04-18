from sqlalchemy import Column, String, Integer
from .database import Base


class Cookie(Base):
    __tablename__ = "cookies"
    id = Column(Integer, primary_key=True)
    message = Column(String)
