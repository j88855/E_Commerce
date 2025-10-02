import os
from dotenv import load_dotenv

load_dotenv()  

# 環境設定
ENV = os.getenv("ENV", "dev")

default_origins = [
    "http://localhost:3000",  # 本地 React/Vue/Next.js
    "http://127.0.0.1:8000",  # 本地 FastAPI 測試
]
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")
if ALLOWED_ORIGINS:
    ALLOWED_ORIGINS = ALLOWED_ORIGINS.split(",")
else:
    ALLOWED_ORIGINS = default_origins

# JWT 設定
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 資料庫設定
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/data.db")