from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from models.order_model import OrderStatus
from typing import List

# === 訂單明細 (下單時用) ===
class OrderProductCreate(BaseModel):
    product_id: int = Field(..., description="商品 ID")
    quantity: int = Field(..., ge=1, description="購買數量")

# === 建立訂單 (傳入用) ===
class OrderCreate(BaseModel):
    products: List[OrderProductCreate]

# === 更新訂單狀態 (PATCH 用) ===
class OrderUpdate(BaseModel):
    status: OrderStatus = Field(..., description="更新訂單狀態")

# === 訂單明細 (查詢時回傳) ===
class OrderProductOut(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)
    
# === 查詢訂單 (回傳用) ===
class OrderOut(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: OrderStatus
    created_at: datetime
    order_products: List[OrderProductOut]

    model_config = ConfigDict(from_attributes=True)