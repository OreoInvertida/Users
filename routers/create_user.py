# users/routes/create_user.py
from fastapi import APIRouter
from models.user_model import UserCreate
from services.user_service import create_user_and_notify

router = APIRouter()

@router.post("/create")
async def create_user(user: UserCreate):
    return await create_user_and_notify(user)
