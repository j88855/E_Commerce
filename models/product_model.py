from sqlalchemy import Integer, String, DECIMAL, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user_model import User
    from models.order_product_model import OrderProduct

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str]= mapped_column(Text, nullable=True)
    price: Mapped[float]= mapped_column(DECIMAL(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    owner: Mapped["User"] = relationship("User", back_populates="products")
    order_products: Mapped[list["OrderProduct"]] = relationship("OrderProduct", back_populates="product")