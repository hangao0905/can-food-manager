from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.models import Flavor as FlavorModel

router = APIRouter(prefix="/flavors", tags=["口味管理"])

@router.get("/")
def list_flavors(brand_code: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(FlavorModel).options(joinedload(FlavorModel.brand))
    if brand_code:
        query = query.filter(FlavorModel.brand_code == brand_code)
    flavors = query.offset(skip).limit(limit).all()
    result = []
    for f in flavors:
        item = {"code": f.code, "name": f.name, "brand_code": f.brand_code, "photo": f.photo, "creator": f.creator, "created_date": f.created_date}
        if f.brand:
            item["brand"] = {"code": f.brand.code, "name": f.brand.name, "created_date": f.brand.created_date}
        result.append(item)
    return result

@router.get("/{flavor_code}")
def get_flavor(flavor_code: int, db: Session = Depends(get_db)):
    flavor = db.query(FlavorModel).options(joinedload(FlavorModel.brand)).filter(FlavorModel.code == flavor_code).first()
    if not flavor:
        raise HTTPException(status_code=404, detail="口味不存在")
    item = {"code": flavor.code, "name": flavor.name, "brand_code": flavor.brand_code, "photo": flavor.photo, "creator": flavor.creator, "created_date": flavor.created_date}
    if flavor.brand:
        item["brand"] = {"code": flavor.brand.code, "name": flavor.brand.name, "created_date": flavor.brand.created_date}
    return item
