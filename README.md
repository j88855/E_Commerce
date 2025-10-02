## 簡介
- 一個使用 FastAPI + SQLAlchemy + PostgreSQL 開發的電商 API，支援使用者、商品、訂單管理，並整合日誌與測試。  
- 本專案支援 Docker 容器化，可直接部署至 Render / Railway / Heroku 等平台。

## 功能
-  使用者註冊 / 登入 / 權限管理（user / seller / admin）
-  商品 CRUD、銷售、存貨管理
-  訂單建立 / 查詢
-  全域例外處理與自訂錯誤
-  RotatingFileHandler 日誌系統
-  pytest 自動化測試
-  Docker + PostgreSQL 容器化部署
-  Swagger / ReDoc API 文件

## 環境需求
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16 (如果不用 Docker，可以自行安裝)

## 本地啟動
1. 複製專案
- git clone https://github.com/<你的帳號>/ecommerce-api.git
- cd ecommerce-api
2. 啟動服務
- docker-compose up --build
3. 打開瀏覽器
- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc

## 測試
- 測試內容包含：
- User：註冊、登入、權限驗證
- Product：CRUD、庫存不足、權限不足
- Order：建立、查詢、錯誤訂單號
- 錯誤情境測試（重複帳號、存貨不足、未授權存取）

## 日誌紀錄
- 所有日誌儲存在 logs/ 目錄
- 採用 RotatingFileHandler，每日自動輪替
- 記錄 API 行為與例外事件

## 專案結構
```
ecommerce_api/
├── alembic/
│   ├── versions/
│   └── env.py
│
├── api/
│   ├── deps.py
│   ├── users_router.py
│   ├── products_router.py
│   └── orders_router.py
│   
├── core/
│   ├── init_data.py
│   ├── logger.py
│   ├── exceptions.py
│   └── security.py
│
├── db/
│   ├── base.py
│   └── session.py
│
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   ├── product_model.py
│   ├── order_model.py
│   └── role_model.py
│
├── repositories/
│   ├── user_repository.py
│   ├── product_repository.py
│   ├── order_repository.py
│   └── role_repository.py
│
├── schemas/
│   ├── user_schema.py
│   ├── product_schema.py
│   └── order_schema.py
│
├── services/
│   ├── user_service.py
│   ├── product_service.py
│   └── order_service.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_products.py
│   └── test_orders.py
│
├── main.py
├── config
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
├── alembic
└── README.md
```
## 作者
馮燁
[Github](https://github.com/j88855)<br>
Email: j88855@yahoo.com.tw
