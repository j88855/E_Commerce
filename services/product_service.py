from sqlalchemy.orm import Session
from schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from repositories.product_repository import ProductRepository
from core.logger import logger
from core.exceptions import ProductNotFound, OutOfStock
from typing import List
from models.user_model import User 

class ProductService:
    @staticmethod
    def create_product(db: Session, product_create: ProductCreate, owner_id: int) -> ProductOut:
        new_product = ProductRepository.create_product(db, product_create, owner_id)
        db.commit()
        db.refresh(new_product)
        logger.info(f"新增商品成功: id: {new_product.id} - name: {new_product.name} - price: {new_product.price} - stock: {new_product.stock}")
        return ProductOut.model_validate(new_product)
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int ) -> ProductOut:
        product = ProductRepository.get_product_by_id(db, product_id)
        if not product:
            logger.warning(f"商品 {product_id} 不存在")
            raise ProductNotFound("商品不存在")
        logger.info(f"取得商品資訊成功: id: {product_id}, name: {product.name}")
        return ProductOut.model_validate(product)
    
    @staticmethod
    def get_products(db: Session, offset: int = 0, limit: int = 20) -> List[ProductOut]:
        products = ProductRepository.get_products(db, offset=offset, limit=limit)
        logger.info(f"取得商品列表: offset={offset}, limit={limit}")
        return [ProductOut.model_validate(p) for p in products]
    
    @staticmethod
    def sell_product(db: Session, product_id: int, quantity: int, current_user: User) -> ProductOut:
        product = ProductRepository.get_product_locked(db, product_id)
        if not product:
            logger.warning(f"商品 {product_id} 不存在")
            raise ProductNotFound("商品不存在")

        if product.stock < quantity:
            logger.warning(f"商品 {product.name} 庫存不足, 現有 {product.stock}, 需求 {quantity}")
            raise OutOfStock(f"{product.name} 庫存不足")
        
        if product.owner_id != current_user.id and current_user.role != "admin":
            raise ProductNotFound("商品不存在")

        product.stock -= quantity
        db.commit()
        db.refresh(product)
        logger.info(f"商品賣出成功: id {product_id}, name: {product.name}")
        return ProductOut.model_validate(product)

    @staticmethod
    def update_product(db: Session, product_id: int, product_update: ProductUpdate, current_user: User) -> ProductOut:
        product = ProductRepository.get_product_by_id(db, product_id)
        if not product:
            logger.warning(f"更新失敗: 商品 {product_id} 不存在")
            raise ProductNotFound("商品不存在")
        if product.owner_id != current_user.id and current_user.role != "admin":
            logger.warning(f"使用者 {current_user.id} 嘗試更新非其擁有的商品 {product_id}")
            raise ProductNotFound("商品不存在")
        update_data = product_update.model_dump(exclude_unset=True)
        updated_product  = ProductRepository.update_product(product, update_data)
        db.commit()
        db.refresh(updated_product)
        logger.info(f"更新商品成功, id: {updated_product.id} - name: {updated_product.name}")
        return ProductOut.model_validate(updated_product)

    @staticmethod
    def delete_product(db: Session, product_id: int, current_user: User) -> None:
        product = ProductRepository.get_product_by_id(db, product_id)
        if not product:
            logger.warning(f"刪除失敗: 商品 {product_id} 不存在")
            raise ProductNotFound("商品不存在")
        if product.owner_id != current_user.id and current_user.role != "admin":
            logger.warning(f"使用者 {current_user.id} 嘗試刪除非其擁有的商品 {product_id}")
            raise ProductNotFound("商品不存在")
        ProductRepository.delete_product(db, product)
        db.commit()
        logger.info(f"刪除商品成功: id:{product.id} - name:{product.name}")