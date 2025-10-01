from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from api.deps import role_required
from models.user_model import User 
from schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from services.product_service import ProductService
from models.user_model import User 
from core.logger import logger
from typing import List
from fastapi import Query

router = APIRouter(prefix="/products", tags=["Products"])
admin_router = APIRouter(prefix="/admin/products", tags=["Admin Products"])

# 快捷別名
admin_required = role_required("admin")
seller_required = role_required("seller")

@router.get("/{product_id}", response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    logger.debug(f"GET /products/{product_id} 被呼叫")
    return ProductService.get_product_by_id(db, product_id)

@router.get("/", response_model=List[ProductOut])
def get_products(offset: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    logger.debug(f"GET /products/ 被呼叫, offset={offset}, limit={limit}")
    return ProductService.get_products(db, offset=offset, limit=limit)

# --- seller ---
@router.post("/", response_model=ProductOut)
def create_product(product_create: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(seller_required)):
    logger.debug(f"POST /products/ 被呼叫, name={product_create.name}")
    return ProductService.create_product(db, product_create, current_user.id)

@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(seller_required)):
    logger.debug(f"PATCH /products/{product_id}被呼叫, 更新資料: {product_update.model_dump(exclude_unset=True)}")
    return ProductService.update_product(db, product_id, product_update, current_user)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(seller_required)):
    logger.debug(f"DELETE /products/{product_id} 被呼叫")
    ProductService.delete_product(db, product_id, current_user)
    return

# --- admin  ---
@admin_router.post("/", response_model=ProductOut)
def create_product(product_create: ProductCreate, db: Session = Depends(get_db), current_admin: User = Depends(admin_required)):
    logger.debug(f"POST /admin/products/ 被呼叫, name={product_create.name}")
    return ProductService.create_product(db, product_create, owner_id=current_admin.id)

@admin_router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db), current_admin: User = Depends(admin_required)):
    logger.debug(f"PATCH /admin/products/{product_id}被呼叫, 更新資料: {product_update.model_dump(exclude_unset=True)}")
    return ProductService.update_product(db, product_id, product_update, current_user=current_admin)

@admin_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_admin: User = Depends(admin_required)):
    logger.debug(f"DELETE /admin/products/{product_id} 被呼叫")
    ProductService.delete_product(db, product_id, current_user=current_admin)
    return