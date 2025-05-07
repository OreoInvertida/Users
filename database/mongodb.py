# users/database/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://oreo:negronauta@users.nppj2o.mongodb.net/?retryWrites=true&w=majority&appName=Users")
DB_NAME = os.getenv("AUTH_DB_NAME", "auth_db")

class MongoDB:
    client = None
    db = None

mongo = MongoDB()

async def connect_to_mongo():
    mongo.client = AsyncIOMotorClient(MONGO_URI)
    mongo.db = mongo.client["carpeta_ciudadana"]
    print("Conexión iniciada.")
