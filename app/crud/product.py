from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

# CREATE
def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# READ all
def get_products(db: Session):
    return db.query(Product).all()

# READ one
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# UPDATE
def update_product(db: Session, product_id: int, product: ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        return None
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

# DELETE
def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        return None
    db.delete(db_product)
    db.commit()
    return db_product
