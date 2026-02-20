from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.models.item import Item, ItemResponse

router = APIRouter(prefix="/items", tags=["Items"])

# In-memory store để test (thực tế dùng DB)
_items_db: dict[int, dict] = {}
_counter: int = 0

@router.get("", response_model=List[ItemResponse])
async def list_items():
    """Lấy danh sách tất cả items."""
    return list(_items_db.values())

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Lấy một item theo ID."""
    if item_id not in _items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return _items_db[item_id]

@router.post("", response_model=ItemResponse, status_code=201)
async def create_item(item: Item):
    """Tạo item mới."""
    global _counter
    _counter += 1
    new_item = {
        **item.model_dump(),
        "id": _counter,
        "created_at": datetime.utcnow(),
    }
    _items_db[_counter] = new_item
    return new_item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    """Cập nhật item."""
    if item_id not in _items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    _items_db[item_id].update({
        **item.model_dump(),
        "id": item_id,
    })
    return _items_db[item_id]

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Xóa item."""
    if item_id not in _items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    del _items_db[item_id]
