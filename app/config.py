import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "wealthwise")
    db_user: str = os.getenv("DB_USER", os.getenv("USER", "postgres"))
    db_password: str = os.getenv("DB_PASSWORD", "")
    
    secret_key: str = os.getenv("SECRET_KEY", "welthwise")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    cache_ttl: int = 300

settings = Settings()
