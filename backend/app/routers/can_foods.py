from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.models import CanFood as CanFoodModel

router = APIRouter(prefix="/can-foods", tags=["罐头管理"])

def to_dict(c):
    r = {
        # 基本信息
        "code": c.code,
        "brand_code": c.brand_code,
        "flavor_code": c.flavor_code,
        "description": c.description,
        # 营养成分（湿基）
        "protein": c.protein,
        "fat": c.fat,
        "ash": c.ash,
        "fiber": c.fiber,
        "moisture": c.moisture,
        "calcium_wet": c.calcium_wet,
        "phosphorus_wet": c.phosphorus_wet,
        "nfe_wet": c.nfe_wet,
        "ca_ph_ratio": c.ca_ph_ratio,
        # 营养成分（干物质）
        "calcium_dm": c.calcium_dm,
        "phosphorus_dm": c.phosphorus_dm,
        "calcium_per_1000kal": c.calcium_per_1000kal,
        "phosphorus_per_1000kal": c.phosphorus_per_1000kal,
        "phosphorus_level": c.phosphorus_level,
        "nfe_dm": c.nfe_dm,
        "protein_dm": c.protein_dm,
        "fat_dm": c.fat_dm,
        "ash_dm": c.ash_dm,
        # 代谢能
        "carb_met_energy_pct": c.carb_met_energy_pct,
        "protein_met_energy_pct": c.protein_met_energy_pct,
        "fat_met_energy_pct": c.fat_met_energy_pct,
        "total_energy_kcal": c.total_energy_kcal,
        "carb_kcal": c.carb_kcal,
        "protein_kcal": c.protein_kcal,
        "fat_kcal": c.fat_kcal,
        "labeled_kcal": c.labeled_kcal,
        # 合格指标
        "protein_pass": c.protein_pass,
        "fat_pass": c.fat_pass,
        "fiber_pass": c.fiber_pass,
        "ash_pass": c.ash_pass,
        "moisture_pass": c.moisture_pass,
        "ca_ph_pass": c.ca_ph_pass,
        "protein_fat_ratio": c.protein_fat_ratio,
        "protein_level": c.protein_level,
        # 其他
        "creator": c.creator,
        "created_date": c.created_date,
        "photo": c.photo,
        # 关联
        "brand": None,
        "flavor": None,
    }
    if c.brand:
        r["brand"] = {"code": c.brand.code, "name": c.brand.name}
    if c.flavor:
        r["flavor"] = {"code": c.flavor.code, "name": c.flavor.name}
    return r

@router.get("/")
def list_can_foods(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    query = db.query(CanFoodModel).options(joinedload(CanFoodModel.brand), joinedload(CanFoodModel.flavor))
    skip = (page - 1) * page_size
    return [to_dict(c) for c in query.offset(skip).limit(page_size).all()]

@router.get("/{code}")
def get_can_food(code: int, db: Session = Depends(get_db)):
    c = db.query(CanFoodModel).options(joinedload(CanFoodModel.brand), joinedload(CanFoodModel.flavor)).filter(CanFoodModel.code == code).first()
    if not c:
        return {"error": "not found"}
    return to_dict(c)
