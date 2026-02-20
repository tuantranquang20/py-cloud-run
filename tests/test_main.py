import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "message" in res.json()

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_readiness():
    res = client.get("/health/ready")
    assert res.status_code == 200
    assert res.json()["ready"] is True

def test_create_item():
    res = client.post("/items", json={
        "name": "Test Item",
        "description": "Item để test CI/CD",
        "price": 99.99,
        "in_stock": True
    })
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Test Item"
    assert data["id"] == 1

def test_get_item():
    res = client.get("/items/1")
    assert res.status_code == 200
    assert res.json()["id"] == 1

def test_get_item_not_found():
    res = client.get("/items/9999")
    assert res.status_code == 404

def test_list_items():
    res = client.get("/items")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_update_item():
    res = client.put("/items/1", json={
        "name": "Updated Item",
        "price": 199.99,
        "in_stock": False
    })
    assert res.status_code == 200
    assert res.json()["price"] == 199.99

def test_delete_item():
    res = client.delete("/items/1")
    assert res.status_code == 204
