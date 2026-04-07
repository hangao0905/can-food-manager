from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.models import Flavor as FlavorModel
from app.routers.auth import get_current_user

router = APIRouter(prefix="/flavors", tags=["口味管理"])

class FlavorUpdate(BaseModel):
    name: Optional[str] = None
    brand_code: Optional[int] = None
    creator: Optional[str] = None
    photo: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/")
def list_flavors(brand_code: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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
def get_flavor(flavor_code: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    flavor = db.query(FlavorModel).options(joinedload(FlavorModel.brand)).filter(FlavorModel.code == flavor_code).first()
    if not flavor:
        raise HTTPException(status_code=404, detail="口味不存在")
    item = {"code": flavor.code, "name": flavor.name, "brand_code": flavor.brand_code, "photo": flavor.photo, "creator": flavor.creator, "created_date": flavor.created_date}
    if flavor.brand:
        item["brand"] = {"code": flavor.brand.code, "name": flavor.brand.name, "created_date": flavor.brand.created_date}
    return item

@router.post("/")
def create_flavor(data: FlavorUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    creator = current_user.get("username", "admin")
    max_code = db.query(FlavorModel.code).order_by(FlavorModel.code.desc()).first()
    new_code = (max_code[0] + 1) if max_code else 1
    flavor = FlavorModel(code=new_code, name=data.name, brand_code=data.brand_code, creator=creator, photo=data.photo)
    db.add(flavor)
    db.commit()
    db.refresh(flavor)
    return {"code": flavor.code, "name": flavor.name, "brand_code": flavor.brand_code, "photo": flavor.photo, "creator": creator, "created_date": flavor.created_date}

@router.put("/{flavor_code}")
def update_flavor(flavor_code: int, data: FlavorUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    flavor = db.query(FlavorModel).filter(FlavorModel.code == flavor_code).first()
    if not flavor:
        raise HTTPException(status_code=404, detail="口味不存在")
    if data.name is not None: flavor.name = data.name
    if data.brand_code is not None: flavor.brand_code = data.brand_code
    if data.photo is not None: flavor.photo = data.photo
    db.commit()
    db.refresh(flavor)
    return {"code": flavor.code, "name": flavor.name, "brand_code": flavor.brand_code, "photo": flavor.photo, "creator": flavor.creator, "created_date": flavor.created_date}

@router.delete("/{flavor_code}")
def delete_flavor(flavor_code: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    flavor = db.query(FlavorModel).filter(FlavorModel.code == flavor_code).first()
    if not flavor:
        raise HTTPException(status_code=404, detail="口味不存在")
    db.delete(flavor)
    db.commit()
    return {"message": "删除成功"}
