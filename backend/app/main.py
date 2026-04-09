from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, brands, flavors, can_foods, countries, users, standards

app = FastAPI(title="Can Food Manager API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 路由
app.include_router(auth, tags=["auth"])
app.include_router(brands, prefix="/api", tags=["brands"])
app.include_router(flavors, prefix="/api", tags=["flavors"])
app.include_router(can_foods, prefix="/api", tags=["can_foods"])
app.include_router(countries, prefix="/api", tags=["countries"])
app.include_router(users, prefix="/api", tags=["users"])
app.include_router(standards, prefix="/api", tags=["standards"])
