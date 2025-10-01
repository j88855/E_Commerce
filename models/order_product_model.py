from sqlalchemy import Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.order_model import Order
    from models.product_model import Product

class OrderProduct(Base):
    __tablename__ = "order_product"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    order: Mapped["Order"] = relationship(back_populates="order_products")
    product: Mapped["Product"] = relationship("Product", back_populates="order_products")