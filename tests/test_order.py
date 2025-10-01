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

def test_order_flow(db):
    # --- 初始化 admin ---
    init_admin(db)
    admin_login = client.post("/users/login", data={"username": "admin", "password": "admin123"})
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}
    # 建立 user & seller
    buyer_headers = register_and_login("buyer", "buyer@test.com")
    seller_headers = register_and_login("seller2", "seller2@test.com")

    # --- admin 幫 seller1 升級角色 ---
    resp = client.patch(f"/admin/users/3/role", params={"role": "seller"}, headers=admin_headers)
    assert resp.status_code == 200

    # seller 建立商品
    product_payload = {"name": "MacBook", "description": "筆電", "price": 60000, "stock": 200}
    resp = client.post("/products", json=product_payload, headers=seller_headers)
    assert resp.status_code == 200
    product_id = resp.json()["id"]

    # buyer 建立訂單
    order_payload = {"products": [{"product_id": product_id, "quantity": 2}]}
    resp = client.post("/orders", json=order_payload, headers=buyer_headers)
    assert resp.status_code == 200
    order_id = resp.json()["id"]

    # buyer 查詢自己的訂單
    resp = client.get(f"/orders/{order_id}", headers=buyer_headers)
    assert resp.status_code == 200
    assert resp.json()["order_products"][0]["product_id"] == product_id
    
    # admin 更新訂單狀態
    update_payload = {"status": "completed"}
    resp = client.patch(f"/admin/orders/{order_id}", json=update_payload, headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"

    # admin 刪除訂單
    resp = client.delete(f"/admin/orders/{order_id}", headers=admin_headers)
    assert resp.status_code == 204