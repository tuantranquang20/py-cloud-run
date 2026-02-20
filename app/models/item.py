from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool
    created_at: datetime
