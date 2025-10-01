from sqlalchemy import Integer, DECIMAL, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from db.base import Base
import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user_model import User
    from models.order_product_model import OrderProduct

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user: Mapped["User"] = relationship("User", back_populates="orders")
    order_products: Mapped[list["OrderProduct"]] = relationship(back_populates="order", cascade="all, delete")