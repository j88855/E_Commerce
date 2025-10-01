from repositories.user_repository import UserRepository
from core.security import hash_password
from schemas.user_schema import UserCreate
from sqlalchemy.orm import Session
from core.logger import logger

def init_admin(db: Session):
    # 預設管理員帳號
    admin_username = "admin"
    admin_email = "admin@example.com"
    admin_password = "admin123"

    existing_admin = UserRepository.get_user_by_username(db, admin_username)
    if not existing_admin:
        hashed = hash_password(admin_password)
        new_admin = UserRepository.create_user(db, UserCreate(
            username=admin_username, email=admin_email, password=admin_password
        ), hashed_password=hashed)
        # 強制設定 role
        new_admin.role = "admin"
        db.commit()
        db.refresh(new_admin)
        logger.info(f"初始化管理員帳號: {admin_username}")