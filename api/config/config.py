#import base setting from pydantic
from pydantic import BaseSettings, AnyHttpUrl
from decouple import config, HS256
from typing import List

#Define CommomnSetting class (inherit from BaseSetting)
class CommonSettings(BaseSettings):
    APP_NAME: str = "/API"
    DEBUG_MODE: bool = True

#Define JWTSetting class(inherit from BaseSetting)
class JWTSettings(BaseSettings):
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast = str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast = str)
    ALGORITHM: "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 #7days
    BACKEND_CORS_ORIGIN: List[AnyHttpUrl] = [
        "http://localhost:8000"
    ]
    PROJECT_NAME: str = "fastAPIDatabase"

#Define the ServerSetting class (inherit from BaseSetting)a
class ServerSettings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 8000

#Define the DatabaseSetting class (inherits from BaseSetting)
class DatabaseSettings(BaseSettings):
    DB_URL: str = config("MONGO_CONNECTION_STRING", cast=str )
    DB_NAME: str = "fastAPIDatabase"

#MainSetting class that includes all the setting classes
class Settings(CommonSettings, JWTSettings, ServerSettings, DatabaseSettings):
    class Config:
        case_sensitive: True
    pass

#create a setting variable that we'll use in the other files
settings = Settings()


