# users/database/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("AUTH_DB_NAME", "carpeta_ciudadana")

class MongoDB:
    client = None
    db = None

mongo = MongoDB()

async def connect_to_mongo():
    mongo.client = AsyncIOMotorClient(MONGO_URI)
    mongo.db = mongo.client["carpeta_ciudadana"]
    print("Conexión iniciada.")
