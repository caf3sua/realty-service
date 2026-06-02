import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "anh_duong_land"
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    S3_ACCESS_KEY_ID: str = "GIHR155UABQHQYA016R2"
    S3_ACCESS_SECRET: str = "APdsXAfLur12i39lbPTQBbZDwsVu1WwNUCqDDAjQ"
    S3_BUCKET: str = "intranet"
    S3_ENDPOINT: str = "https://s3-hcmc02.higiocloud.vn"
    S3_REGION: str = "hanoi"
    S3_VERIFY: bool = True

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
