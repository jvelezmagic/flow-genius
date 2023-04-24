from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str = "Flow Genius API"
    description: str = "API for Flow Genius"
    version: str = "0.1.0"
    debug: bool = False
    openai_api_key: str = ""
    ai21_api_key: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
