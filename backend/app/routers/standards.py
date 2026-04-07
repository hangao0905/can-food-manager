from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.database import get_db
from app.models.models import Standard

router = APIRouter(prefix="/standards", tags=["计算标准"])

class StandardUpdate(BaseModel):
    name: Optional[str] = None
    field: Optional[str] = None
    operator: Optional[str] = None
    threshold: Optional[float] = None
    threshold_max: Optional[float] = None
    unit: Optional[str] = None
    status: Optional[str] = None
    created_date: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/")
def list_standards(db: Session = Depends(get_db)):
    return db.query(Standard).order_by(Standard.id).all()

@router.put("/{id}")
def update_standard(id: int, data: StandardUpdate, db: Session = Depends(get_db)):
    s = db.query(Standard).filter(Standard.id == id).first()
    if not s:
        raise HTTPException(status_code=404, detail="标准不存在")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(s, field, value)
    db.commit()
    db.refresh(s)
    return s

# 内置默认标准（用于初始化）
DEFAULT_STANDARDS = [
    {"name": "粗蛋白合格",        "field": "protein",             "operator": ">=", "threshold": 0.10,   "unit": ""},
    {"name": "粗脂肪合格",        "field": "fat",                "operator": "<=", "threshold": 0.09,   "unit": ""},
    {"name": "粗纤维合格",        "field": "fiber",              "operator": "<=", "threshold": 0.03,   "unit": ""},
    {"name": "粗灰分合格",        "field": "ash",                "operator": "<=", "threshold": 0.02,   "unit": ""},
    {"name": "含水量合格",        "field": "moisture",           "operator": "<=", "threshold": 0.80,   "unit": ""},
    {"name": "钙磷比合格",        "field": "ca_ph_ratio",        "operator": "range","threshold": 1.1, "threshold_max": 1.4, "unit": ""},
    {"name": "磷含量指标-高",     "field": "phosphorus_per_1000kal","operator":">","threshold":2400,"unit":"mg/1000kcal"},
    {"name": "磷含量指标-低",     "field": "phosphorus_per_1000kal","operator":"<","threshold":1800,"unit":"mg/1000kcal"},
    {"name": "蛋白质:脂肪-优秀",  "field": "protein_fat_ratio",  "operator": ">",  "threshold": 3.0,    "unit": ""},
    {"name": "蛋白质:脂肪-一般",  "field": "protein_fat_ratio",  "operator": ">",  "threshold": 1.5,    "unit": ""},
]

@router.post("/init")
def init_defaults(db: Session = Depends(get_db)):
    """初始化默认标准（已存在则跳过）"""
    existing = db.query(Standard).count()
    if existing > 0:
        return {"message": f"已有 {existing} 条标准，跳过初始化"}
    for d in DEFAULT_STANDARDS:
        s = Standard(**d)
        db.add(s)
    db.commit()
    return {"message": f"已初始化 {len(DEFAULT_STANDARDS)} 条标准"}
