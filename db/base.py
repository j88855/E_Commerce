from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """所有 ORM model 繼承這個 Base"""
    pass