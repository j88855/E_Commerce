from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from core.logger import logger
from core.exceptions import UserAlreadyExists, UserNotFound, InvalidPassword, InvalidToken, ProductNotFound, OrderNotFound
from api.routers import user_router, product_router, order_router
from contextlib import asynccontextmanager
from db.session import engine
from db.base import Base
from db.session import engine, SessionLocal
from core.init_data import init_admin
from config import ALLOWED_ORIGINS

# 啟動事件：初始化管理員帳號
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動前初始化
    print("App starting...")
    Base.metadata.create_all(engine)

    # 建立 DB session，初始化管理員帳號
    db = SessionLocal()
    try:
        init_admin(db)
    except Exception as e:
        logger.error(f"初始化管理員失敗: {e}")
    finally:
        db.close()
    yield
    # 關閉前清理
    print("App shutting down...")

app = FastAPI(title="E-commerce API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 正式環境改成前端網址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 掛載 router
app.include_router(user_router.router)
app.include_router(user_router.admin_router)
app.include_router(product_router.router)
app.include_router(product_router.admin_router)
app.include_router(order_router.router)
app.include_router(order_router.admin_router)

# 全域 Exception Handler
@app.exception_handler(UserAlreadyExists)
@app.exception_handler(UserNotFound)
@app.exception_handler(InvalidPassword)
@app.exception_handler(InvalidToken)
@app.exception_handler(ProductNotFound)
@app.exception_handler(OrderNotFound)
async def http_exception_handler(request: Request, exc):  
    # 記錄到 logger
    logger.warning(f"{request.method} {request.url} 發生錯誤: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})