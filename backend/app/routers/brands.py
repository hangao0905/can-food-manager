from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Brand as BrandModel

router = APIRouter(prefix="/brands", tags=["品牌管理"])

@router.get("/")
def list_brands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    brands = db.query(BrandModel).offset(skip).limit(limit).all()
    return [{"code": b.code, "name": b.name, "created_date": b.created_date} for b in brands]

@router.get("/{brand_code}")
def get_brand(brand_code: int, db: Session = Depends(get_db)):
    brand = db.query(BrandModel).filter(BrandModel.code == brand_code).first()
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    return {"code": brand.code, "name": brand.name, "created_date": brand.created_date}
