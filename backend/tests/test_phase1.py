import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Base

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "SMART BUILD" in data["message"]
    assert "version" in data

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "SMART BUILD" in data["service"]

def test_db_check_endpoint():
    response = client.get("/api/db-check")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "connected"
    assert data["database"] == "online"
    assert data["registered_tables_count"] >= 24
    assert "users" in data["tables"]
    assert "products" in data["tables"]
    assert "orders" in data["tables"]
    assert "ai_estimations" in data["tables"]
    assert "enquiries" in data["tables"]

def test_all_24_tables_defined():
    table_names = set(Base.metadata.tables.keys())
    expected_tables = {
        "users",
        "customer_profiles",
        "supplier_profiles",
        "delivery_partner_profiles",
        "categories",
        "products",
        "product_images",
        "inventory",
        "carts",
        "cart_items",
        "addresses",
        "orders",
        "order_items",
        "payments",
        "deliveries",
        "reviews",
        "wishlists",
        "wishlist_items",
        "notifications",
        "complaints",
        "price_history",
        "ai_estimations",
        "ai_predictions",
        "audit_logs",
        "enquiries"
    }
    assert expected_tables.issubset(table_names), f"Missing tables: {expected_tables - table_names}"
