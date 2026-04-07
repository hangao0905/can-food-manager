from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.models import CanFood as CanFoodModel

router = APIRouter(prefix="/can-foods", tags=["罐头管理"])

def to_dict(c):
    r = {"code": c.code, "brand_code": c.brand_code, "flavor_code": c.flavor_code, "description": c.description}
    r["protein"] = c.protein
    r["fat"] = c.fat
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
