#Imports
from fastapi import FastAPI
import uvicorn
from api.routers import get_api_router
from config import settings

app = FastAPI()

#include our  API router
app.include_router(get_api_router(app), tags=["products"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE
        )
