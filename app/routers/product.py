from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.crud import product as crud

router = APIRouter(prefix="/products", tags=["Products"])

# CREATE
@router.post("/", response_model=ProductResponse)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

# READ all
@router.get("/", response_model=list[ProductResponse])
def read_all(db: Session = Depends(get_db)):
    db_products = crud.get_products(db)
    if not db_products:
        raise HTTPException(status_code=404, detail="No products found")
    return db_products

# READ one
@router.get("/{product_id}", response_model=ProductResponse)
def read(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product 

@router.patch("/{product_id}", response_model=ProductResponse)
def update(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    deleted_product = crud.delete_product(db, product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}
