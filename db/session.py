from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from config import DATABASE_URL

# 建立 SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session, future=True)

# 提供 FastAPI 依賴注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()