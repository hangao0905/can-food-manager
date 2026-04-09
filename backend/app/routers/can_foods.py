from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List, Optional

from app.database import get_db
from app.models.models import CanFood as CanFoodModel
from app.models.models import Flavor as FlavorModel
from app.models.models import Brand as BrandModel
from app.schemas.schemas import CanFood, CanFoodCreate, CanFoodUpdate

router = APIRouter(prefix="/can-foods", tags=["罐头管理"])


@router.get("/", response_model=List[CanFood])
def list_can_foods(
    brand_code: int = None,
    flavor_code: int = None,
    description: str = None,
    min_protein: float = None,
    max_protein: float = None,
    min_fat: float = None,
    max_fat: float = None,
    protein_pass: str = None,
    page: int = 1,
    page_size: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(CanFoodModel).options(
        joinedload(CanFoodModel.flavor).joinedload(FlavorModel.brand),
        joinedload(CanFoodModel.brand)
    )
    
    if brand_code:
        query = query.filter(CanFoodModel.brand_code == brand_code)
    if flavor_code:
        query = query.filter(CanFoodModel.flavor_code == flavor_code)
    if description:
        query = query.filter(CanFoodModel.description.contains(description))
    if min_protein is not None:
        query = query.filter(CanFoodModel.protein >= min_protein)
    if max_protein is not None:
        query = query.filter(CanFoodModel.protein <= max_protein)
    if min_fat is not None:
        query = query.filter(CanFoodModel.fat >= min_fat)
    if max_fat is not None:
        query = query.filter(CanFoodModel.fat <= max_fat)
    if protein_pass is not None:
        query = query.filter(CanFoodModel.protein_pass == protein_pass)
    
    skip = (page - 1) * page_size
    can_foods = query.offset(skip).limit(page_size).all()
    
    return can_foods


@router.get("/{can_food_code}", response_model=CanFood)
def get_can_food(can_food_code: int, db: Session = Depends(get_db)):
    can_food = db.query(CanFoodModel).options(
        joinedload(CanFoodModel.flavor).joinedload(FlavorModel.brand),
        joinedload(CanFoodModel.brand)
    ).filter(CanFoodModel.code == can_food_code).first()
    if not can_food:
        raise HTTPException(status_code=404, detail="罐头不存在")
    return can_food


@router.post("/", response_model=CanFood)
def create_can_food(can_food: CanFoodCreate, db: Session = Depends(get_db)):
    db_can_food = CanFoodModel(**can_food.model_dump())
    db.add(db_can_food)
    db.commit()
    db.refresh(db_can_food)
    return db_can_food


@router.put("/{can_food_code}", response_model=CanFood)
def update_can_food(can_food_code: int, can_food: CanFoodUpdate, db: Session = Depends(get_db)):
    db_can_food = db.query(CanFoodModel).filter(CanFoodModel.code == can_food_code).first()
    if not db_can_food:
        raise HTTPException(status_code=404, detail="罐头不存在")
    for key, value in can_food.model_dump(exclude_unset=True).items():
        setattr(db_can_food, key, value)
    db.commit()
    db.refresh(db_can_food)
    return db_can_food


@router.delete("/{can_food_code}")
def delete_can_food(can_food_code: int, db: Session = Depends(get_db)):
    db_can_food = db.query(CanFoodModel).filter(CanFoodModel.code == can_food_code).first()
    if not db_can_food:
        raise HTTPException(status_code=404, detail="罐头不存在")
    db.delete(db_can_food)
    db.commit()
    return {"message": "罐头已删除"}
