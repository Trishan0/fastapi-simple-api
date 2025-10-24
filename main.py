from fastapi import FastAPI
from models import Product
from database import session, engine
import database_models

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

products : list= [
    Product(id=1, name="Laptop", description="A high-end laptop", price=1500.00, in_stock=True),
    Product(id=2, name="Smartphone", description="A latest model smartphone", price=800.00, in_stock=True),
    Product(id=3, name="Headphones", description="Noise-cancelling headphones", price=200.00, in_stock=False),
    Product(id=4, name="Monitor", description="4K UHD Monitor", price=400.00, in_stock=True),
]

@app.get("/products")
def get_all_products():
    db = session()
    return products

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product.id == product_id:
            print(f"Product found : {product}")
            return product
    return {"error":"Product not found"}

@app.post("/products")
def add_product(product: Product):
    products.append(product)
    print(f"New product added : {product}")
    return product

@app.put("/products")
def update_product(product_id: int, updated_product: Product):
    for i in range (len(products)):
        if products[i].id == product_id:
            products[i] = updated_product
            return {"message": "Product Updaed Successfully"}
    return {"error":"Product not found"}

@app.delete("/products")
def delete_product(product_id: int):
    for i in range(len(products)):
        if products[i].id == product_id:
            del products[i]
            return {"message": "Product Deleted Successfully"}
    return {"error":"Product not found"}
