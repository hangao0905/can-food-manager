from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Brand as BrandModel
from app.schemas.schemas import Brand, BrandCreate, BrandUpdate

router = APIRouter(prefix="/brands", tags=["品牌管理"])


@router.get("/", response_model=List[Brand])
def list_brands(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    brands = db.query(BrandModel).offset(skip).limit(limit).all()
    return brands


@router.get("/{brand_code}", response_model=Brand)
def get_brand(brand_code: int, db: Session = Depends(get_db)):
    brand = db.query(BrandModel).filter(BrandModel.code == brand_code).first()
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    return brand


@router.post("/", response_model=Brand)
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    db_brand = db.query(BrandModel).filter(BrandModel.name == brand.name).first()
    if db_brand:
        raise HTTPException(status_code=400, detail="品牌已存在")
    db_brand = BrandModel(**brand.model_dump())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


@router.put("/{brand_code}", response_model=Brand)
def update_brand(brand_code: int, brand: BrandUpdate, db: Session = Depends(get_db)):
    db_brand = db.query(BrandModel).filter(BrandModel.code == brand_code).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    for key, value in brand.model_dump(exclude_unset=True).items():
        setattr(db_brand, key, value)
    db.commit()
    db.refresh(db_brand)
    return db_brand


@router.delete("/{brand_code}")
def delete_brand(brand_code: int, db: Session = Depends(get_db)):
    db_brand = db.query(BrandModel).filter(BrandModel.code == brand_code).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    db.delete(db_brand)
    db.commit()
    return {"message": "品牌已删除"}
