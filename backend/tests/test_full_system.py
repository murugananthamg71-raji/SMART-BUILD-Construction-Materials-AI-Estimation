import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token(email="customer@smartbuild.com", password="Demo1234!"):
    res = client.post("/api/auth/login", json={"email": email, "password": password})
    return res.json()["access_token"]

def test_list_categories():
    res = client.get("/api/categories")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 9
    names = [c["name"] for c in data]
    assert any("Cement" in n for n in names)
    assert any("Steel" in n for n in names)

def test_list_products():
    res = client.get("/api/products")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 20
    assert len(data["items"]) > 0

def test_product_search_and_filter():
    res = client.get("/api/products?search=UltraTech")
    assert res.status_code == 200
    items = res.json()["items"]
    assert any("UltraTech" in item["name"] for item in items)

def test_cart_operations():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Clear cart first
    client.delete("/api/cart", headers=headers)

    # Get a product
    prods = client.get("/api/products").json()["items"]
    prod = prods[0]

    # Add to cart
    add_res = client.post("/api/cart/items", json={"product_id": prod["id"], "quantity": 5}, headers=headers)
    assert add_res.status_code == 200
    cart_data = add_res.json()
    assert cart_data["item_count"] == 5
    assert float(cart_data["subtotal"]) > 0
    assert float(cart_data["tax_amount"]) > 0

def test_order_creation_and_stock_reduction():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Ensure 1 item in cart
    prods = client.get("/api/products").json()["items"]
    prod = prods[0]
    initial_stock = prod["inventory"]["stock"]

    client.delete("/api/cart", headers=headers)
    client.post("/api/cart/items", json={"product_id": prod["id"], "quantity": 2}, headers=headers)

    # Place order
    order_res = client.post("/api/orders", json={
        "payment_method": "cod",
        "notes": "Testing order placement"
    }, headers=headers)
    assert order_res.status_code == 201
    order_data = order_res.json()
    assert "SB-" in order_data["order_number"]
    assert order_data["status"] == "confirmed"
    assert len(order_data["items"]) == 1

    # Check that stock reduced by 2
    updated_prod = client.get(f"/api/products/{prod['id']}").json()
    assert updated_prod["inventory"]["stock"] == initial_stock - 2

def test_ai_estimator_calculation():
    payload = {
        "building_length": 40.0,
        "building_width": 30.0,
        "no_of_floors": 2,
        "floor_height": 10.0,
        "construction_type": "Residential",
        "building_type": "Individual House",
        "location": "Bangalore",
        "quality_preference": "Standard"
    }
    res = client.post("/api/estimator/calculate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["built_up_area_sqft"] == 2400.0  # 40 * 30 * 2
    assert data["cement_bags"] > 0
    assert data["steel_kg"] > 0
    assert data["bricks_count"] > 0
    assert data["estimated_total_budget"] > 0
    assert len(data["breakdown"]) == 7

def test_admin_dashboard():
    token = get_auth_token("admin@smartbuild.com", "Demo1234!")
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/api/admin/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total_users"] >= 4
    assert data["total_products"] >= 20
    assert data["total_orders"] >= 1

def test_supplier_dashboard():
    token = get_auth_token("supplier@smartbuild.com", "Demo1234!")
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/api/supplier/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total_products"] > 0

def test_delivery_partner_deliveries():
    token = get_auth_token("delivery@smartbuild.com", "Demo1234!")
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/api/deliveries/assigned", headers=headers)
    assert res.status_code == 200
    deliveries = res.json()
    assert len(deliveries) >= 1
