from sqlalchemy import select
from sqlalchemy.orm import Session
from models.product_model import Product
from schemas.product_schema import ProductCreate
from typing import List

class ProductRepository:
    @staticmethod
    def create_product(db: Session, product: ProductCreate, owner_id: int) -> Product:
        new_product = Product(owner_id=owner_id, name=product.name, description=product.description, price=product.price, stock=product.stock)
        db.add(new_product)
        return new_product
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        return db.scalars(stmt).first()
    
    @staticmethod
    def get_products(db: Session, offset: int = 0, limit: int = 20) -> List[Product]:
        stmt = select(Product).offset(offset).limit(limit)
        return db.scalars(stmt).all()
    
    @staticmethod
    def get_product_locked(db: Session, product_id: int) -> Product | None:
        return db.query(Product).where(Product.id == product_id).with_for_update().first()

    @staticmethod
    def update_product(product: Product, update_data: dict) -> Product | None:
        for key, value in update_data.items():
            setattr(product, key, value)
        return product

    @staticmethod
    def delete_product(db: Session, product: Product) -> None:
        db.delete(product)