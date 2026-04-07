from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, SessionLocal
from app.routers import brands, flavors, can_foods, standards, auth, users

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
app.include_router(standards.router)
app.include_router(auth.router)
app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    from app.models.models import User
    from app.routers.auth import hash_password
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            admin = User(username="admin", password_hash=hash_password("admin123"), role="admin", status="active")
            db.add(admin)
            db.commit()
            print("默认管理员已创建: admin / admin123")
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "罐头信息管理系统 API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
