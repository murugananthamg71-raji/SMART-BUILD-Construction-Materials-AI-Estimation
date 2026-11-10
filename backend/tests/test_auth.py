import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_customer():
    unique_email = f"ramesh_{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "Ramesh Kumar",
        "email": unique_email,
        "password": "Password123!",
        "phone": "+919876543210",
        "role": "customer"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == unique_email
    assert data["user"]["role"] == "customer"

def test_register_duplicate_email():
    unique_email = f"dup_{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "First User",
        "email": unique_email,
        "password": "Password123!",
        "role": "customer"
    }
    # Register once
    res1 = client.post("/api/auth/register", json=payload)
    assert res1.status_code == 201

    # Attempt second registration with identical email
    res2 = client.post("/api/auth/register", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]

def test_login_success():
    payload = {
        "email": "customer@smartbuild.com",
        "password": "Demo1234!"
    }
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "customer"

def test_login_invalid_password():
    payload = {
        "email": "customer@smartbuild.com",
        "password": "WrongPassword!"
    }
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 401

def test_get_current_user_profile():
    login_res = client.post("/api/auth/login", json={
        "email": "customer@smartbuild.com",
        "password": "Demo1234!"
    })
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "customer@smartbuild.com"

def test_register_supplier():
    unique_email = f"bharat_{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "Bharat Steels Ltd",
        "email": unique_email,
        "password": "SupplierPass123!",
        "phone": "+918888888888",
        "role": "supplier",
        "company_name": "Bharat Steels & Cement",
        "city": "Mumbai"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["role"] == "supplier"
    assert data["user"]["supplier_profile"]["company_name"] == "Bharat Steels & Cement"
    assert data["user"]["supplier_profile"]["approval_status"] == "pending"
