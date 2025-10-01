from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate, UserLogin, UserUpdate, UserOut, AdminUserOut
from services.user_service import UserService
from api.deps import get_current_user, role_required
from db.session import get_db
from core.logger import logger

router = APIRouter(prefix="/users", tags=["Users"])
admin_router = APIRouter(prefix="/admin/users", tags=["Admin Users"])

# 快捷別名
admin_required = role_required("admin")
seller_required = role_required("seller")

@router.post("/register", response_model=UserOut)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    logger.debug(f"POST /users/register 被呼叫, username={user_create.username}")
    return UserService.register(db, user_create)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.debug(f"POST /users/login 被呼叫, username={form_data.username}")
    access_token = UserService.login(db, form_data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    logger.debug("GET /users/me 被呼叫")
    return UserOut(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        created_at=current_user.created_at
    )

@router.patch("/me", response_model=UserOut)
def update_me(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.debug(f"PATCH /users/me 被呼叫, 更新資料: {user_update.model_dump(exclude_unset=True)}")
    return UserService.update_me(db, current_user, user_update)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    UserService.delete_me(db, current_user)
    logger.debug(f"使用者刪除成功: id={current_user.id}")
    return

# --- admin ---

@admin_router.get("/", response_model=list[AdminUserOut])
def get_all_users(db: Session = Depends(get_db), _: User  = Depends(admin_required)):
    logger.debug("GET /admin/users 被呼叫")
    return UserService.get_all_users(db)

@admin_router.get("/{user_id}", response_model=AdminUserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    logger.debug(f"GET /admin/users/{user_id} 被呼叫")
    return UserService.get_user_by_id(db, user_id)

@admin_router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    logger.debug(f"PATCH /admin/users/{user_id} 被呼叫, 更新資料: {user_update.model_dump(exclude_unset=True)}")
    return UserService.update_user(db, user_id, user_update)

@admin_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    UserService.delete_user(db, user_id)
    logger.debug(f"DELETE /admin/users/{user_id} 被呼叫")
    return

@admin_router.patch("/{user_id}/role", response_model=AdminUserOut)
def update_user_role(user_id: int, role: str, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    logger.debug(f"PATCH /admin/users/{user_id}/role 被呼叫, 更新角色資料: {role}")
    return UserService.update_user_role(db, user_id, role)