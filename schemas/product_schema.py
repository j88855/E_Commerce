from pydantic import BaseModel, Field, StringConstraints, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=100)] = Field(..., description="商品名稱, 1~100字")
    description: Annotated[str, StringConstraints(max_length=9999)] = Field(description="商品描述")
    price: float = Field(..., gt=0, description="商品價格, 必須 > 0")
    stock: int = Field(..., ge=0, description="庫存量, 必須 >= 0")

class ProductUpdate(BaseModel):
    name: Optional[Annotated[str, StringConstraints(min_length=1, max_length=100)]] = Field(default=None, description="商品名稱, 1~100字")
    description: Optional[Annotated[str, StringConstraints(max_length=9999)]] = Field(default=None, description="商品描述, 最多9999字")
    price: Optional[float] = Field(default=None, gt=0, description="商品價格, 必須 > 0")
    stock: Optional[int] = Field(default=None, ge=0, description="庫存量, 必須 >= 0")

class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float  
    stock: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)