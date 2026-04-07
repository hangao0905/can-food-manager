from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.models import CanFood as CanFoodModel

router = APIRouter(prefix="/can-foods", tags=["罐头管理"])

class CanFoodUpdate(BaseModel):
    brand_code: Optional[int] = None
    flavor_code: Optional[int] = None
    description: Optional[str] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    ash: Optional[float] = None
    fiber: Optional[float] = None
    moisture: Optional[float] = None
    calcium_wet: Optional[float] = None
    phosphorus_wet: Optional[float] = None
    nfe_wet: Optional[float] = None
    ca_ph_ratio: Optional[float] = None
    calcium_dm: Optional[float] = None
    phosphorus_dm: Optional[float] = None
    calcium_per_1000kal: Optional[float] = None
    phosphorus_per_1000kal: Optional[float] = None
    phosphorus_level: Optional[str] = None
    nfe_dm: Optional[float] = None
    protein_dm: Optional[float] = None
    fat_dm: Optional[float] = None
    ash_dm: Optional[float] = None
    carb_met_energy_pct: Optional[float] = None
    protein_met_energy_pct: Optional[float] = None
    fat_met_energy_pct: Optional[float] = None
    total_energy_kcal: Optional[float] = None
    carb_kcal: Optional[float] = None
    protein_kcal: Optional[float] = None
    fat_kcal: Optional[float] = None
    labeled_kcal: Optional[float] = None
    protein_pass: Optional[str] = None
    fat_pass: Optional[str] = None
    fiber_pass: Optional[str] = None
    ash_pass: Optional[str] = None
    moisture_pass: Optional[str] = None
    ca_ph_pass: Optional[str] = None
    protein_fat_ratio: Optional[float] = None
    protein_level: Optional[str] = None
    creator: Optional[str] = None
    created_date: Optional[str] = None
    photo: Optional[str] = None

    class Config:
        from_attributes = True

def to_dict(c):
    r = {
        "code": c.code, "brand_code": c.brand_code, "flavor_code": c.flavor_code,
        "description": c.description, "protein": c.protein, "fat": c.fat,
        "ash": c.ash, "fiber": c.fiber, "moisture": c.moisture,
        "calcium_wet": c.calcium_wet, "phosphorus_wet": c.phosphorus_wet,
        "nfe_wet": c.nfe_wet, "ca_ph_ratio": c.ca_ph_ratio,
        "calcium_dm": c.calcium_dm, "phosphorus_dm": c.phosphorus_dm,
        "calcium_per_1000kal": c.calcium_per_1000kal,
        "phosphorus_per_1000kal": c.phosphorus_per_1000kal,
        "phosphorus_level": c.phosphorus_level, "nfe_dm": c.nfe_dm,
        "protein_dm": c.protein_dm, "fat_dm": c.fat_dm, "ash_dm": c.ash_dm,
        "carb_met_energy_pct": c.carb_met_energy_pct,
        "protein_met_energy_pct": c.protein_met_energy_pct,
        "fat_met_energy_pct": c.fat_met_energy_pct,
        "total_energy_kcal": c.total_energy_kcal,
        "carb_kcal": c.carb_kcal, "protein_kcal": c.protein_kcal,
        "fat_kcal": c.fat_kcal, "labeled_kcal": c.labeled_kcal,
        "protein_pass": c.protein_pass, "fat_pass": c.fat_pass,
        "fiber_pass": c.fiber_pass, "ash_pass": c.ash_pass,
        "moisture_pass": c.moisture_pass, "ca_ph_pass": c.ca_ph_pass,
        "protein_fat_ratio": c.protein_fat_ratio, "protein_level": c.protein_level,
        "creator": c.creator, "created_date": c.created_date, "photo": c.photo,
        "brand": None, "flavor": None,
    }
    if c.brand:
        r["brand"] = {"code": c.brand.code, "name": c.brand.name}
    if c.flavor:
        r["flavor"] = {"code": c.flavor.code, "name": c.flavor.name}
    return r

@router.get("/")
def list_can_foods(page: int = 1, page_size: int = 50, db: Session = Depends(get_db)):
    query = db.query(CanFoodModel).options(joinedload(CanFoodModel.brand), joinedload(CanFoodModel.flavor))
    skip = (page - 1) * page_size
    return [to_dict(c) for c in query.offset(skip).limit(page_size).all()]

@router.get("/{code}")
def get_can_food(code: int, db: Session = Depends(get_db)):
    c = db.query(CanFoodModel).options(joinedload(CanFoodModel.brand), joinedload(CanFoodModel.flavor)).filter(CanFoodModel.code == code).first()
    if not c:
        return {"error": "not found"}
    return to_dict(c)

@router.put("/{code}")
def update_can_food(code: int, data: CanFoodUpdate, db: Session = Depends(get_db)):
    c = db.query(CanFoodModel).filter(CanFoodModel.code == code).first()
    if not c:
        raise HTTPException(status_code=404, detail="罐头不存在")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(c, field, value)
    db.commit()
    db.refresh(c)
    return to_dict(c)

@router.delete("/{code}")
def delete_can_food(code: int, db: Session = Depends(get_db)):
    c = db.query(CanFoodModel).filter(CanFoodModel.code == code).first()
    if not c:
        raise HTTPException(status_code=404, detail="罐头不存在")
    db.delete(c)
    db.commit()
    return {"message": "删除成功"}
