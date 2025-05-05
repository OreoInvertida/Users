# users/main.py

from fastapi import FastAPI
from routers.create_user import router as create_user_router
from database.mongodb import connect_to_mongo

app = FastAPI(title="Users Microservice")

@app.on_event("startup")
async def startup_event():
    print("→ Conectando a MongoDB...")
    await connect_to_mongo()
    print("✅ Conexión iniciada.")

app.include_router(create_user_router, prefix="/users", tags=["Users"])
