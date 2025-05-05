from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def clear_database():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await client.drop_database("carpeta_ciudadana")

asyncio.run(clear_database())