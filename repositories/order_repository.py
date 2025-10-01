from sqlalchemy import select
from sqlalchemy.orm import Session
from models.order_model import Order
from models.product_model import Product
from schemas.order_schema import OrderUpdate
from models.order_product_model import OrderProduct
from typing import List

class OrderRepository:
    @staticmethod
    def create_order(db: Session, user_id: int, total_price: float) -> Order:
        new_order = Order(user_id=user_id, total_price=total_price)
        db.add(new_order)
        db.flush()  # 取得 order.id
        return new_order

    @staticmethod
    def create_order_product(db: Session, order_id: int, product_id: int, quantity: int, unit_price: float) -> OrderProduct:    
        order_product = OrderProduct(order_id=order_id, product_id=product_id, quantity=quantity, unit_price=unit_price)
        db.add(order_product)
        return order_product

    @staticmethod
    def update_product_stock(db: Session, product: Product, quantity: int) -> None:
        product.stock -= quantity

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)
        return db.scalars(stmt).first()
    
    @staticmethod
    def get_orders_by_user_id(db: Session, user_id: int, offset: int = 0, limit: int = 20) -> List[Order]:
        stmt = select(Order).where(Order.user_id == user_id).offset(offset).limit(limit)
        return db.scalars(stmt).all()
    
    @staticmethod
    def get_all_orders(db: Session, offset: int = 0, limit: int = 20) -> List[Order]:
        stmt = select(Order).offset(offset).limit(limit)
        return db.scalars(stmt).all()
    
    @staticmethod
    def update_order_status(db: Session, order: Order, order_update: OrderUpdate) -> Order:
        order.status = order_update.status
        return order
    
    @staticmethod
    def delete_order(db: Session, order: Order) -> None:
        db.delete(order)