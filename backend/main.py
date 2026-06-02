from fastapi import FastAPI, Depends
from models import Product
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import database_models as database_models


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hello, World!"

products = [
    Product(id=1, name="Laptop", price=999.99, description="A high-performance laptop.", quantity=10),
    Product(id=2, name="Smartphone", price=499.99, description="A powerful smartphone with a great camera.", quantity=20),
    Product(id=3, name="Headphones", price=199.99, description="Noise-cancelling over-ear headphones.", quantity=15)
] 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()

    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
    db.commit()
init_db()

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
        
    return "product not found"

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:  
        return "No Product Found"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter
    (database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    else:
        return "No Product Found"