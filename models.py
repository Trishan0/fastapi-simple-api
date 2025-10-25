from pydantic import BaseModel

class ProductBase(BaseModel):
    id: int
    name: str
    description : str | None
    price : float
    in_stock : bool = False