# users/services/user_service.py
from database.mongodb import mongo
from models.user_model import UserCreate
from utils.logger import logger
from fastapi import HTTPException
import httpx
from dotenv import load_dotenv
import os
import json

#load_dotenv()

EXTERNAL_REGISTER_URL = os.getenv("EXTERNAL_REGISTER_URL")
NOTIFICATIONS_URL = os.getenv("NOTIFICATIONS_URL")

OPERATOR_ID = os.getenv("OPERATOR_ID")
OPERATOR_NAME = os.getenv("OPERATOR_NAME")

async def create_user_and_notify(user_data: UserCreate):
    if mongo.db is None:
        raise Exception("La conexión a MongoDB no está disponible.")

    collection = mongo.db["users"]

    # Verificar si el usuario ya existe
    existing = await collection.find_one({"id": user_data.id})
    if existing:
        logger.warning("Usuario ya existe en la base de datos")
        raise HTTPException(status_code=409, detail="El usuario ya está registrado en la base de datos local.")

    existing_email = await collection.find_one({"email": user_data.email})
    if existing_email:
        raise HTTPException(status_code=409, detail="El correo ya está registrado.")

    # Guardar localmente
    user_dict = user_data.dict()
    user_dict["type"] = "citizen"

    # Guardar en MongoDB
    result = await collection.insert_one(user_dict)
    logger.info(f"Usuario creado localmente con ID DB: {result.inserted_id}")

    # Enviar a API externa
    payload = {
        "id": user_data.id,
        "name": user_data.name,
        "address": user_data.address,
        "email": user_data.email,
        "operatorId": OPERATOR_ID,
        "operatorName": OPERATOR_NAME
    }



    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"→ Enviando usuario a API externa: {EXTERNAL_REGISTER_URL}")
            
            headers = {"Content-Type": "application/json"}
            payload_clean = {
                "id": int(user_data.id),
                "name": str(user_data.name).strip(),
                "address": str(user_data.address).strip(),
                "email": str(user_data.email).strip(),
                "operatorId": OPERATOR_ID,
                "operatorName": OPERATOR_NAME
            }

            response = await client.post(f"{EXTERNAL_REGISTER_URL}/registerCitizen/", json=payload_clean, headers=headers)
            
            logger.info(f"← Respuesta API externa: {response.status_code} - {response.text}")

            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error registrando usuario en la API externa: {response.text}"
                )

        except httpx.RequestError as e:
            logger.error(f"Error de conexión con API externa: {e}")
            raise HTTPException(status_code=503, detail="Fallo de conexión con la API externa.")
        
        # Notificar por correo al usuario
        try:
            logger.info(f"→ Enviando correo de bienvenida a {user_data.email}")
            await client.post(f"{NOTIFICATIONS_URL}/send", json={
                "email": user_data.email,
                "name": user_data.name
            })
        except Exception as e:
            logger.error(f"Error enviando notificación por correo: {e}")
            raise HTTPException(status_code=502, detail="No se pudo enviar la notificación de bienvenida.")

            

    return {"message": "Usuario creado, reportado y notificado exitosamente."}
