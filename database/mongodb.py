# users/database/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
class MongoDB:
    client = None
    db = None

mongo = MongoDB()

async def connect_to_mongo():
    conn = os.getenv("MONGO_URI")
    mongo.client = AsyncIOMotorClient(conn)
    mongo.db = mongo.client["carpeta_ciudadana"]
    print("Conexión iniciada.")
