from pydantic import BaseModel


class CookieBase(BaseModel):
    message: str


class CookieCreate(CookieBase):
    pass


class Cookie(CookieBase):
    id: int

    class Config:
        orm_mode = True
