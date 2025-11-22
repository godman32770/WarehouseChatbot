from pydantic import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: str
    mysql_url: str

    class Config:
        env_file = ".env" 