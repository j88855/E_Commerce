from sqlalchemy.orm import Session
from schemas.order_schema import OrderCreate, OrderUpdate, OrderOut
from models.product_model import Product
from repositories.order_repository import OrderRepository
from core.logger import logger
from core.exceptions import ProductNotFound, OutOfStock, OrderNotFound
from typing import List
from models.user_model import User

class OrderService:
    @staticmethod
    def create_order(db: Session, user_id: int, order_create: OrderCreate) -> OrderOut:
        total_price = 0.0
        products_cache = {}

        # 1. 驗證商品並計算總價
        for item in order_create.products:
            product = db.get(Product, item.product_id)
            if not product:
                raise ProductNotFound(f"商品 {item.product_id} 不存在")
            if product.stock < item.quantity:
                raise OutOfStock(f"商品 {product.name} 庫存不足, 需求 {item.quantity}, 現有 {product.stock}")
            total_price += float(product.price) * item.quantity
            products_cache[item.product_id] = product  # 存起來避免重查

        # 2. 建立訂單主檔
        new_order = OrderRepository.create_order(db, user_id, total_price)

        # 3. 建立訂單明細 + 扣庫存
        for item in order_create.products:
            product: Product = products_cache[item.product_id]
            OrderRepository.create_order_product(
                db,
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product.price
                )
            OrderRepository.update_product_stock(db, product, item.quantity)

        db.commit()
        db.refresh(new_order)
        logger.info(f"新增訂單成功: id={new_order.id}, user_id={user_id}, total_price={new_order.total_price}, status={new_order.status}")
        return OrderOut.model_validate(new_order)
    
    @staticmethod
    def get_order_by_id(db: Session, order_id: int, current_user: User) -> OrderOut:
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            logger.warning(f"訂單 {order_id} 不存在")
            raise OrderNotFound("訂單不存在")
        if order.user_id != current_user.id and current_user.role != "admin":
            logger.warning(f"使用者 {current_user.id} 不存在 {order_id} 訂單")
            raise OrderNotFound("訂單不存在")
        logger.info(f"取得訂單成功: id:{order_id}")
        return OrderOut.model_validate(order)
    
    @staticmethod
    def get_all_orders(db: Session, offset: int = 0, limit: int = 20) -> List[OrderOut]:
        orders = OrderRepository.get_all_orders(db, offset=offset, limit=limit)
        logger.info(f"取得訂單列表: {len(orders)} 筆, offset={offset}, limit={limit}")
        return [OrderOut.model_validate(o) for o in orders]
    
    @staticmethod
    def get_my_orders(db: Session, current_user: User, offset: int = 0, limit: int = 20) -> List[OrderOut]:
        orders = OrderRepository.get_orders_by_user_id(db, current_user.id, offset, limit)
        logger.info(f"使用者 {current_user.id} 取得自己的訂單: {len(orders)} 筆")
        return [OrderOut.model_validate(o) for o in orders]

    @staticmethod
    def update_order_status(db: Session, order_id: int, order_update: OrderUpdate) -> OrderOut:        
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            logger.warning(f"更新失敗: 訂單 {order_id} 不存在")
            raise OrderNotFound("訂單不存在")
        order.status = order_update.status
        db.commit()
        db.refresh(order)
        logger.info(f"更新訂單成功: id: {order_id}, user_id: {order.user_id}, status: {order.status}")
        return OrderOut.model_validate(order)
    
    @staticmethod
    def delete_order(db: Session, order_id: int) -> None:
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            logger.warning(f"刪除失敗: 訂單 {order_id} 不存在")
            raise OrderNotFound("訂單不存在")
        user_id, status = order.user_id, order.status # 避免 delete 後 instance 變成 deleted 狀態
        OrderRepository.delete_order(db, order)
        db.commit()
        logger.info(f"刪除訂單成功: id:{order.id}, user_id:{user_id}, status: {status}")