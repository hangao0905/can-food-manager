from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import brands, flavors, can_foods

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="罐头信息管理系统", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(brands.router)
app.include_router(flavors.router)
app.include_router(can_foods.router)


@app.get("/")
def root():
    return {"message": "罐头信息管理系统 API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
