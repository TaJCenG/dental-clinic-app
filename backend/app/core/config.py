from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # Database
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    # JWT
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # OTP
    otp_expire_minutes: int

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()