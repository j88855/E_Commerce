from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from api.deps import get_current_user, role_required
from schemas.order_schema import OrderCreate, OrderUpdate, OrderOut
from services.order_service import OrderService
from core.logger import logger
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])
admin_router = APIRouter(prefix="/admin/orders", tags=["Admin Orders"])

# 快捷別名
admin_required = role_required("admin")
seller_required = role_required("seller")

@router.post("/", response_model=OrderOut)
def create_order(order_create: OrderCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    logger.debug(f"POST /orders/ 被呼叫, user_id={current_user.id}")
    return OrderService.create_order(db, current_user.id, order_create)

@router.get("/{order_id}", response_model=OrderOut)
def get_order_by_id(order_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    logger.debug(f"GET /orders/{order_id} 被呼叫, user_id={current_user.id}")
    return OrderService.get_order_by_id(db, order_id, current_user)

# --- admin ---
@admin_router.get("/", response_model=List[OrderOut])
def get_all_orders(db: Session = Depends(get_db), _: str = Depends(admin_required)):
    logger.debug("GET /admin/orders 被呼叫")
    return OrderService.get_all_orders(db)

@admin_router.patch("/{order_id}", response_model=OrderOut)
def update_order_status(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db), _: str = Depends(admin_required)):
    logger.debug(f"PATCH /admin/orders/{order_id} 被呼叫, 更新狀態: {order_update.status}")
    return OrderService.update_order_status(db, order_id, order_update)

@admin_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db), _: str = Depends(admin_required)):
    logger.debug(f"DELETE /admin/orders/{order_id} 被呼叫")
    OrderService.delete_order(db, order_id)
    return