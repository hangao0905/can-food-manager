from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.models import Flavor as FlavorModel
from app.schemas.schemas import Flavor, FlavorCreate, FlavorUpdate
from pydantic import BaseModel

router = APIRouter(prefix="/flavors", tags=["口味管理"])

class FlavorListResponse(BaseModel):
    total: int
    data: List[Flavor]


@router.get("/", response_model=FlavorListResponse)
def list_flavors(name: str = None, brand_code: int = None, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    query = db.query(FlavorModel).options(joinedload(FlavorModel.brand))
    if brand_code:
        query = query.filter(FlavorModel.brand_code == brand_code)
    if name:
        query = query.filter(FlavorModel.name.like(f"%{name}%"))
    total = query.count()
    flavors = query.offset(skip).limit(limit).all()
    return FlavorListResponse(total=total, data=flavors)


@router.get("/{flavor_code}", response_model=Flavor)
def get_flavor(flavor_code: int, db: Session = Depends(get_db)):
    flavor = db.query(FlavorModel).options(joinedload(FlavorModel.brand)).filter(FlavorModel.code == flavor_code).first()
    if not flavor:
        raise HTTPException(status_code=404, detail="口味不存在")
    return flavor


@router.post("/", response_model=Flavor)
def create_flavor(flavor: FlavorCreate, db: Session = Depends(get_db)):
    db_flavor = FlavorModel(**flavor.model_dump())
    db.add(db_flavor)
    db.commit()
    db.refresh(db_flavor)
    return db_flavor


@router.put("/{flavor_code}", response_model=Flavor)
def update_flavor(flavor_code: int, flavor: FlavorUpdate, db: Session = Depends(get_db)):
    db_flavor = db.query(FlavorModel).filter(FlavorModel.code == flavor_code).first()
    if not db_flavor:
        raise HTTPException(status_code=404, detail="口味不存在")
    for key, value in flavor.model_dump(exclude_unset=True).items():
        setattr(db_flavor, key, value)
    db.commit()
    db.refresh(db_flavor)
    return db_flavor


@router.delete("/{flavor_code}")
def delete_flavor(flavor_code: int, db: Session = Depends(get_db)):
    db_flavor = db.query(FlavorModel).filter(FlavorModel.code == flavor_code).first()
    if not db_flavor:
        raise HTTPException(status_code=404, detail="口味不存在")
    db.delete(db_flavor)
    db.commit()
    return {"message": "口味已删除"}
