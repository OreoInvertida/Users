# users/database/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    client = None
    db = None

mongo = MongoDB()

async def connect_to_mongo():
    mongo.client = AsyncIOMotorClient("mongodb://localhost:27017")
    mongo.db = mongo.client["carpeta_ciudadana"]
    print("Conexión iniciada.")
