# users/models/user_model.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    name: str
    email: str
    address: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    address: str | None = None

class UserInDB(UserCreate):
    _id: str | None = None
