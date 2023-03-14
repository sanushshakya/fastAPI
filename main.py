#Imports
from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from api.routers import get_api_router
from config import settings

app = FastAPI()

#Startup Event
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]

#Shutdown Event
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

#include our  API router
app.include_router(get_api_router(app), tags=["products"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE
        )
