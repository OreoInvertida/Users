from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test_mongo():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["carpeta_ciudadana"]
    print(await db.list_collection_names())

asyncio.run(test_mongo())
