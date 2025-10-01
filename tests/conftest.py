import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from db.base import Base

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session, future=True)

@pytest.fixture(scope="function")
def db():
    # 每次測試前建表
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)