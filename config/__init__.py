#import base setting from pydantic
from pydantic import BaseSettings

#Define CommomnSetting class (inherit from BaseSetting)
class CommonSettings(BaseSettings):
    APP_NAME: str = "API"
    DEBUG_MODE: bool = True

#Define the ServerSetting class (inherit from BaseSetting)
class ServerSettings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 5000

#Define the DatabaseSetting class (inherits from BaseSetting)
class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb+srv://shakyasanush7:#MongoDb47@cluster0.5ikyk9f.mongodb.net/?retryWrites=true&w=majority"
    DB_NAME: str = "fastAPIDatabase"

#MainSetting class that includes all the setting classes
class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass

#create a setting variable that we'll use in the other files
settings = Settings()


