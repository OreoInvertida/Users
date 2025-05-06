# users/routers/user_crud.py
from fastapi import APIRouter, Depends
from models.user_model import UserCreate, UserUpdate
from services.user_create_service import create_user_and_notify
from services.user_rud_service import get_user_by_id, update_user, delete_user
from services.token_service import verify_token

router = APIRouter()

@router.post("/create")
async def create_user(user: UserCreate):
    return await create_user_and_notify(user)

@router.get("/get/{user_id}")
async def read_user(user_id: int, payload: dict = Depends(verify_token)):
    return await get_user_by_id(user_id)

@router.put("/update/{user_id}")
async def modify_user(user_id: int, updates: UserUpdate, payload: dict = Depends(verify_token)):
    return await update_user(user_id, updates)

@router.delete("/delete/{user_id}")
async def remove_user(user_id: int, payload: dict = Depends(verify_token)):
    return await delete_user(user_id)
