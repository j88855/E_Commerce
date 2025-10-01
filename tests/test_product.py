import pytest
from fastapi.testclient import TestClient
from main import app
from db.session import get_db
from core.init_data import init_admin

@pytest.fixture(autouse=True)
def override_get_db(db):
    app.dependency_overrides[get_db] = lambda: db
    yield
    app.dependency_overrides[get_db] = get_db

client = TestClient(app)

def register_and_login(username="testuser", email="test@example.com", password="password"):
    payload = {"username": username, "email": email, "password": password}
    resp = client.post("/users/register", json=payload)
    assert resp.status_code == 200
    login_payload = {"username": username, "password": password}
    resp = client.post("/users/login", data=login_payload)
    assert resp.status_code == 200
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}

def test_product_crud(db):
    # 登入 admin
    init_admin(db)
    admin_login = client.post("/users/login", data={"username": "admin", "password": "admin123"})
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}
    
    # 註冊 seller 帳號
    seller_headers = register_and_login("seller1", "seller1@test.com")
    
    # admin 把這個帳號升級成 seller
    resp = client.patch(f"/admin/users/2/role", params={"role": "seller"}, headers=admin_headers)
    assert resp.status_code == 200
        
    # 建立商品
    product_payload = {"name": "iPhone 16", "description": "pro", "price": 40000, "stock": 200}
    resp = client.post("/products", json=product_payload, headers=seller_headers)
    assert resp.status_code == 200
    product_id = resp.json()["id"]

    # 查詢單一商品
    resp = client.get(f"/products/{product_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "iPhone 16"

    # 更新商品
    update_payload = {"name": "iPhone 16 Pro", "description": "pro max", "price": 45000, "stock": 200}
    resp = client.patch(f"/products/{product_id}", json=update_payload, headers=seller_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "iPhone 16 Pro"

    # 商品列表
    resp = client.get("/products")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # 刪除商品
    resp = client.delete(f"/products/{product_id}", headers=seller_headers)
    assert resp.status_code == 204