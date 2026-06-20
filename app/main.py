from fastapi import FastAPI
from app.routers import product
from app.routers import auth
from app.db.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(product.router)
app.include_router(auth.router)