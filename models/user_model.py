# users/models/user_model.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    name: str
    email: str
    address: str
    password: str

class UserInDB(UserCreate):
    _id: str | None = None
