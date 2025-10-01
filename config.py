import os

# 環境設定
ENV = os.getenv("ENV", "dev")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# JWT 設定
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 資料庫設定
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://ecommerce_user:ecommerce_pass@localhost:5432/ecommerce_db")