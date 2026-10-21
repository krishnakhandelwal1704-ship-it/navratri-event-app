import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "NAVRATRI 2026 API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./navratri.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_jwt_key_navratri_2026_dandiya")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

settings = Settings()