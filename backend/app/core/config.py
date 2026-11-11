from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "SMART BUILD - AI-Powered Construction Material Ordering System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "smart_build_super_secret_jwt_key_2026_change_in_production_xyz123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    # Default to MySQL; SQLite fallback supported seamlessly
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://root:password@localhost:3306/smart_build"
    )
    USE_SQLITE_FALLBACK: bool = True

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.31.63:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://smart-build.vercel.app"
    ]

    # Payment Gateway (Sandbox)
    RAZORPAY_KEY_ID: str = "rzp_test_placeholder_key"
    RAZORPAY_KEY_SECRET: str = "rzp_test_placeholder_secret"

    # AI Estimator Defaults
    ENABLE_AI_PREDICTIONS: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

settings = Settings()
