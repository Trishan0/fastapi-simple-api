from fastapi import FastAPI, Depends
from models import ProductBase
from database import session, engine
import database_models
from sqlalchemy.orm import Session 
from pathlib import Path
import json
app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)


sample_data_path =  Path(__file__).with_name("sample_data.json")
with sample_data_path.open("r", encoding="utf-8") as sample_file:
    sample_data =json.load(sample_file)  

products = [ProductBase(**item) for item in sample_data]

def get_db():
    try:
        db=session()
        yield db
    finally:
        db.close()    

# Initialize database with sample products
def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    
init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    # db = session()
    return db_products

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==product_id).first()
    if db_product:
        return db_product
    return {"error":"Product not found"}

@app.post("/products")
def add_product(product: ProductBase, db:Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    print(f"New product added : {product}")
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: ProductBase, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==product_id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.in_stock = updated_product.in_stock
        db.commit()    
        return {"message": "Product Updaed Successfully"}
    return {"error":"Product not found"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product Deleted Successfully"}
    return {"error":"Product not found"}
