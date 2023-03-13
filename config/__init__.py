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

#MainSetting class that includes all the setting classes
class Settings(CommonSettings, ServerSettings):
    pass

#create a setting variable that we'll use in the other files
settings = Settings()


