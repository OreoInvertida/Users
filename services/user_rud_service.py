# users/services/user_crud_service.py
from database.mongodb import mongo
from fastapi import HTTPException
from models.user_model import UserUpdate

async def get_user_by_id(user_id: int):
    collection = mongo.db["users"]
    user = await collection.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.pop("_id")
    user["id"] = str(user["id"])
    return user

async def get_user_by_email(user_email: str):
    collection = mongo.db["users"]
    user = await collection.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user["_id"] = str(user["_id"])
    return user

async def update_user(user_id: int, updates: UserUpdate):
    collection = mongo.db["users"]
    data = {k: v for k, v in updates.dict().items() if v is not None}
    result = await collection.update_one({"id": user_id}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario actualizado exitosamente."}

async def delete_user(user_id: int):
    collection = mongo.db["users"]
    result = await collection.delete_one({"id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente."}
