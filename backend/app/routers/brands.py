from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.models import Brand as BrandModel
from app.routers.auth import get_current_user

router = APIRouter(prefix="/brands", tags=["品牌管理"])

class BrandUpdate(BaseModel):
    name: Optional[str] = None
    alias: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    created_date: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/")
def list_brands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    brands = db.query(BrandModel).offset(skip).limit(limit).all()
    return [{"code": b.code, "name": b.name, "alias": b.alias, "logo": b.logo, "description": b.description, "country": b.country, "created_date": b.created_date} for b in brands]

@router.get("/{brand_code}")
def get_brand(brand_code: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    brand = db.query(BrandModel).filter(BrandModel.code == brand_code).first()
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    return {"code": brand.code, "name": brand.name, "alias": brand.alias, "logo": brand.logo, "description": brand.description, "country": brand.country, "created_date": brand.created_date}

@router.post("/")
def create_brand(data: BrandUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    max_code = db.query(BrandModel.code).order_by(BrandModel.code.desc()).first()
    new_code = (max_code[0] + 1) if max_code else 1
    brand = BrandModel(code=new_code, name=data.name, alias=data.alias, logo=data.logo, description=data.description, country=data.country or '国内', created_date=data.created_date)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return {"code": brand.code, "name": brand.name, "alias": brand.alias, "logo": brand.logo, "description": brand.description, "country": brand.country, "created_date": brand.created_date}

@router.put("/{brand_code}")
def update_brand(brand_code: int, data: BrandUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    brand = db.query(BrandModel).filter(BrandModel.code == brand_code).first()
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    if data.name is not None: brand.name = data.name
    if data.alias is not None: brand.alias = data.alias
    if data.logo is not None: brand.logo = data.logo
    if data.description is not None: brand.description = data.description
    if data.country is not None: brand.country = data.country
    if data.created_date is not None: brand.created_date = data.created_date
    db.commit()
    db.refresh(brand)
    return {"code": brand.code, "name": brand.name, "alias": brand.alias, "logo": brand.logo, "description": brand.description, "country": brand.country, "created_date": brand.created_date}

@router.delete("/{brand_code}")
def delete_brand(brand_code: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    brand = db.query(BrandModel).filter(BrandModel.code == brand_code).first()
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    db.delete(brand)
    db.commit()
    return {"message": "删除成功"}
