from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    database_url:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    class Config:
        env_file = ".env"

settings = Setting()