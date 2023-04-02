#Imports
from fastapi import FastAPI
import uvicorn
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from api.routers import get_api_router
from api.config.config import settings

#models
from api.models.user_model import User

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.APP_NAME}/openapi.json"
)

#Startup Event
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]

    await init_beanie(
        document_models= [
            User
        ]
    )

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
