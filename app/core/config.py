import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "anh_duong_land"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    GOOGLE_CLIENT_ID: str = ""

    S3_ACCESS_KEY_ID: str = "GIHR155UABQHQYA016R2"
    S3_ACCESS_SECRET: str = "APdsXAfLur12i39lbPTQBbZDwsVu1WwNUCqDDAjQ"
    S3_BUCKET: str = "intranet"
    S3_ENDPOINT: str = "https://s3-hcmc02.higiocloud.vn"
    S3_REGION: str = "hanoi"
    S3_VERIFY: bool = True

    SECRET_KEY: str = "7ef5bfd6205ba8fcd0e0f865db26a117b8f972b9a101f30a9db58673a3c9e6c9"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
