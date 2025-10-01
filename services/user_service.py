from core.security import hash_password, verify_password, create_access_token, decode_access_token
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from models.user_model import User
from schemas.user_schema import UserCreate, UserLogin, UserUpdate, UserOut, AdminUserOut
from core.exceptions import UserAlreadyExists, EmailAlreadyExists, UserNotFound, InvalidPassword, InvalidToken
from core.logger import logger

class UserService:
    @staticmethod
    def register(db: Session, user_create: UserCreate) -> UserOut:
        existing_user = UserRepository.get_user_by_username(db, user_create.username)
        if existing_user:
            logger.warning(f"使用者註冊失敗: {user_create.username} 已存在")
            raise UserAlreadyExists("使用者已存在")
        hashed = hash_password(user_create.password)
        new_user = UserRepository.create_user(db, user_create, hashed)
        db.commit()
        db.refresh(new_user)
        logger.info(f"使用者註冊成功: {user_create.username} (id={new_user.id})")
        return UserOut.model_validate(new_user)
        # model_validate 自動驗證 + 轉型
        # 但schema的 Out 要加 model_config = ConfigDict(from_attributes=True)
    
    @staticmethod
    def login(db: Session, user_login: UserLogin) -> str:
        user = UserRepository.get_user_by_username(db, user_login.username)
        if not user:
            logger.warning(f"登入失敗: 使用者 {user_login.username} 不存在")
            raise UserNotFound("使用者不存在")
        is_valid = verify_password(user_login.password, user.hashed_password)
        if not is_valid:
            logger.warning(f"登入失敗: 使用者 {user_login.username} 密碼錯誤")
            raise InvalidPassword("密碼錯誤")
        token_data = {"user_id": user.id}
        access_token = create_access_token(token_data)
        logger.info(f"使用者登入成功: {user.username} (id={user.id})")
        return access_token

    @staticmethod
    def get_current_user(db: Session, token: str) -> User:
        payload = decode_access_token(token)
        if not payload or "user_id" not in payload:
            logger.warning("Token 無效")
            raise InvalidToken("Token 無效")
        user_id  = payload["user_id"]
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            logger.warning(f"Token 對應的使用者不存在 (user_id: {user_id})")
            raise UserNotFound("使用者不存在")
        logger.info(f"取得使用者資訊成功: {user.username} id: {user.id}")
        return user

    @staticmethod
    def update_me(db: Session, current_user: User, user_update: UserUpdate) -> UserOut:
        update_fields = user_update.model_dump(exclude_unset=True)
        #model_dump會回傳一個 dict
        #exclude_unset=True 只包含有被使用者傳入的欄位（未傳入的欄位就不會包含在 dict 裡）
        if "username" in update_fields:
            existing_user = UserRepository.get_user_by_username(db, update_fields["username"])
            if existing_user and existing_user.id != current_user.id:
                logger.warning(f"使用者更新 username 失敗: {existing_user.username} 已存在")
                raise UserAlreadyExists("使用者名稱已存在")
        if "email" in update_fields:
            existing_user = UserRepository.get_user_by_email(db, update_fields["email"])
            if existing_user and existing_user.id != current_user.id:
                logger.warning(f"使用者更新 email 失敗: {existing_user.email} 已存在")
                raise EmailAlreadyExists("電子郵件已存在")
        if "password" in update_fields:
            update_fields["hashed_password"] = hash_password(update_fields.pop("password"))
        updated_user = UserRepository.update_user(current_user, update_fields)
        db.commit()
        db.refresh(updated_user)
        logger.info(f"更新使用者資訊成功: username: {user_update.username}")
        return UserOut.model_validate(updated_user)
    
    @staticmethod
    def delete_me(db: Session, current_user: User) -> None:
        UserRepository.delete_user(db, current_user)
        db.commit()
        logger.info(f"刪除使用者成功: id:{current_user.id}, username:{current_user.username}")
        
    # --- admin ---
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int ) -> UserOut:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            logger.warning(f"使用者 {user_id} 不存在")
            raise UserNotFound("使用者不存在")
        logger.info(f"取得使用者資訊成功: id {user.id}, username{user.username}, ")
        return AdminUserOut.model_validate(user)
    
    @staticmethod
    def get_all_users(db: Session) -> list[AdminUserOut]:
        users = UserRepository.get_all_users(db)
        logger.info("取得所有使用者資訊成功")
        return [AdminUserOut.model_validate(u) for u in users]
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserOut:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            logger.warning(f"更新失敗: 使用者 {user_id} 不存在")
            raise UserNotFound("使用者不存在")
        update_fields = user_update.model_dump(exclude_unset=True)

        if "username" in update_fields:
            existing_user = UserRepository.get_user_by_username(db, update_fields["username"])
            if existing_user and existing_user.id != user_id:
                logger.warning(f"使用者更新 username 失敗: {existing_user.username} 已存在")
                raise UserAlreadyExists("使用者名稱已存在")
        if "email" in update_fields:
            existing_user = UserRepository.get_user_by_email(db, update_fields["email"])
            if existing_user and existing_user.id != user_id:
                logger.warning(f"使用者更新 email 失敗: {existing_user.email} 已存在")
                raise EmailAlreadyExists("電子郵件已存在")           
        if "password" in update_fields:
            update_fields["hashed_password"] = hash_password(update_fields.pop("password"))
        updated_user = UserRepository.update_user(user, update_fields)        
        db.commit()
        db.refresh(updated_user)
        logger.info(f"管理員更新使用者成功: id: {updated_user.id} - username: {updated_user.username}")
        return AdminUserOut.model_validate(updated_user)
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            logger.warning(f"刪除失敗: 使用者 {user_id} 不存在")
            raise UserNotFound("使用者不存在")
        UserRepository.delete_user(db, user)
        db.commit()
        logger.info(f"管理員刪除使用者成功: id:{user_id} - username:{user.username}")

    @staticmethod
    def update_user_role(db: Session, user_id: int, role: str) -> AdminUserOut:
        updated_user = UserRepository.get_user_by_id(db, user_id)
        if not updated_user:
            logger.warning(f"更新使用者角色失敗: 使用者 {user_id} 不存在")
            raise UserNotFound("使用者不存在")
        updated = UserRepository.update_user(updated_user, {"role": role})
        db.commit()
        db.refresh(updated)
        logger.info(f"更新使用者角色: id={updated.id}, role={role}")
        return AdminUserOut.model_validate(updated)