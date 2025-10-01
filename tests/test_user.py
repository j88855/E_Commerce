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

def register_user(username="test", email="test@example.com", password="password"):
    payload = {"username": username, "email": email, "password": password}
    resp = client.post("/users/register", json=payload)
    return resp

def login_user(username="test", password="password"):
    payload = {"username": username, "password": password}
    resp = client.post("/users/login", data=payload)
    return resp

# 註冊 & 登入
def test_register_and_login():
    # 註冊成功
    resp = register_user()
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "test"
    assert "id" in data

    # 註冊重複
    resp = register_user()
    assert resp.status_code == 400
    assert "使用者已存在" in resp.text

    # 登入成功
    resp = login_user()
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # 登入失敗 - 密碼錯誤
    resp = login_user(password="wrongxxx")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "密碼錯誤"

    # 登入失敗 - 使用者不存在
    resp = login_user(username="notfound")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "使用者不存在"

# /me 權限保護 & 更新刪除自己
def test_me_update_delete():
    # 註冊 + 登入
    register_user()
    token = login_user().json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # /me 正常
    resp = client.get("/users/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["username"] == "test"

    # /me 無效 token
    resp = client.get("/users/me", headers={"Authorization": "Bearer invalid"})
    assert resp.status_code == 401
    assert "Token 無效" in resp.text

    # 更新自己
    update_payload = {"username": "new_test", "email": "new_test@example.com"}
    resp = client.patch("/users/me", json=update_payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "new_test"
    assert data["email"] == "new_test@example.com"

    # 刪除自己
    resp = client.delete("/users/me", headers=headers)
    assert resp.status_code == 204

    # /me 應該找不到
    resp = client.get("/users/me", headers=headers)
    assert resp.status_code == 401
    assert "使用者不存在" in resp.text


# 管理員 CRUD 使用者
def test_admin_crud_user(db):
    # 初始化管理員
    init_admin(db)

    # 登入管理員
    login_payload = {"username": "admin", "password": "admin123"}
    resp = client.post("/users/login", data=login_payload)
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 建立兩個一般使用者
    resp1 = register_user("user1", "user1@test.com")
    user1_id = resp1.json()["id"]
    resp2 = register_user("user2", "user2@test.com")
    user2_id = resp2.json()["id"]

    # 更新使用者
    resp = client.patch(f"/admin/users/{user1_id}", json={"username": "user1_new", "email": "user1_new@test.com"}, headers=headers)
    assert resp.status_code == 200

    # 更新不存在使用者
    resp = client.patch("/admin/users/9999", json={"username": "nonexist"}, headers=headers)
    assert resp.status_code == 404

    # 更新成重複 username/email
    resp = client.patch(f"/admin/users/{user1_id}", json={"username": "user2"}, headers=headers)
    assert resp.status_code == 400
    resp = client.patch(f"/admin/users/{user1_id}", json={"email": "user2@test.com"}, headers=headers)
    assert resp.status_code == 400

    # 更新角色
    resp = client.patch(f"/admin/users/{user1_id}/role", params={"role": "admin"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["role"] == "admin"

    # 刪除使用者
    resp = client.delete(f"/admin/users/{user1_id}", headers=headers)
    assert resp.status_code == 204