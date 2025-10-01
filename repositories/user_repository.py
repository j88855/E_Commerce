from sqlalchemy import select
from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate

class UserRepository:
    @staticmethod
    def create_user(db: Session, user: UserCreate, hashed_password: str) -> User:
        new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(new_user)
        return new_user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return db.scalars(stmt).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return db.scalars(stmt).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.scalars(stmt).first()
        
    @staticmethod
    def get_all_users(db: Session) -> list[User]:
        stmt = select(User)
        return db.scalars(stmt).all()
    
    @staticmethod
    def update_user(user: User, update_data: dict) -> User:
        allowed_fields = {"username", "email", "hashed_password", "role"}
        for key, value in update_data.items():
            if key in allowed_fields:
                setattr(user, key, value)
        return user
        #setattr 對每一個傳進來要更新的欄位都自動設定設定物件屬性。
        #class User:
            #def __init__(self, username, email):
                #self.username = username
                #self.email = email
        #user = User("tom", "tom@test.com")
        # 原本寫法
        #user.username = "jerry"
        # 等效寫法
        #setattr(user, "username", "jerry")            
    
    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        db.delete(user)