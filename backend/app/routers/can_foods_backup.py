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
    min_phosphorus: float = None,
    max_phosphorus: float = None,
    protein_pass: str = None,
    fat_pass: str = None,
    fiber_pass: str = None,
    ash_pass: str = None,
    moisture_pass: str = None,
    ca_ph_pass: str = None,
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
    if min_phosphorus is not None:
        query = query.filter(CanFoodModel.phosphorus_wet >= min_phosphorus)
    if max_phosphorus is not None:
        query = query.filter(CanFoodModel.phosphorus_wet <= max_phosphorus)
    if protein_pass is not None:
        query = query.filter(CanFoodModel.protein_pass == protein_pass)
    if fat_pass is not None:
        query = query.filter(CanFoodModel.fat_pass == fat_pass)
    if fiber_pass is not None:
        query = query.filter(CanFoodModel.fiber_pass == fiber_pass)
    if ash_pass is not None:
        query = query.filter(CanFoodModel.ash_pass == ash_pass)
    if moisture_pass is not None:
        query = query.filter(CanFoodModel.moisture_pass == moisture_pass)
    if ca_ph_pass is not None:
        query = query.filter(CanFoodModel.ca_ph_pass == ca_ph_pass)
    
    skip = (page - 1) * page_size
    can_foods = query.offset(skip).limit(page_size).all()
    
    return can_foods


@router.post("/recalc-all")
def recalc_all_can_foods(db: Session = Depends(get_db)):
    """重新计算所有罐头的派生字段"""
    can_foods = db.query(CanFoodModel).all()
    count = 0
    for can_food in can_foods:
        calculate_can_food(db, can_food)
        count += 1
    db.commit()
    return {"message": f"重新计算完成，共处理 {count} 条记录"}


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
    # 创建后自动计算派生字段
    db_can_food = calculate_can_food(db, db_can_food)
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
    # 更新后自动重新计算派生字段
    db_can_food = calculate_can_food(db, db_can_food)
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


def calculate_can_food(db: Session, can_food: CanFoodModel) -> CanFoodModel:
    """根据营养数据计算派生字段"""
    from app.models.models import Standard as StandardModel
    
    # 获取所有启用的标准
    standards = db.query(StandardModel).filter(StandardModel.status == 'active').all()
    standards_map = {s.field: s for s in standards}
    
    # 计算无抽出物 NFE (湿基) = 100 - protein - fat - ash - fiber - moisture
    if all(x is not None for x in [can_food.protein, can_food.fat, can_food.ash, can_food.fiber, can_food.moisture]):
        can_food.nfe_wet = 100 - can_food.protein - can_food.fat - can_food.ash - can_food.fiber - can_food.moisture
    
    # 计算干物质 DM = 100 - moisture
    dm = 100 - can_food.moisture if can_food.moisture is not None else None
    
    # 计算钙磷比 ca_ph_ratio = calcium_wet / phosphorus_wet
    if can_food.calcium_wet is not None and can_food.phosphorus_wet is not None and can_food.phosphorus_wet > 0:
        can_food.ca_ph_ratio = can_food.calcium_wet / can_food.phosphorus_wet
    
    # 计算干物质基础指标
    if dm and dm > 0:
        if can_food.protein is not None:
            can_food.protein_dm = (can_food.protein / dm) * 100
        if can_food.fat is not None:
            can_food.fat_dm = (can_food.fat / dm) * 100
        if can_food.ash is not None:
            can_food.ash_dm = (can_food.ash / dm) * 100
        if can_food.nfe_wet is not None:
            can_food.nfe_dm = (can_food.nfe_wet / dm) * 100
        if can_food.calcium_wet is not None:
            can_food.calcium_dm = (can_food.calcium_wet / dm) * 100
        if can_food.phosphorus_wet is not None:
            can_food.phosphorus_dm = (can_food.phosphorus_wet / dm) * 100
    
    # 计算能量 (单位: kcal/100g)
    # 蛋白: 4 kcal/g, 脂肪: 9 kcal/g, 碳水(碳水化合物): 4 kcal/g
    protein_kcal = can_food.protein * 4 if can_food.protein else 0
    fat_kcal = can_food.fat * 9 if can_food.fat else 0
    nfe_kcal = can_food.nfe_wet * 4 if can_food.nfe_wet else 0
    can_food.total_energy_kcal = protein_kcal + fat_kcal + nfe_kcal
    can_food.protein_kcal = protein_kcal
    can_food.fat_kcal = fat_kcal
    can_food.carb_kcal = nfe_kcal
    
    # 计算能量百分比
    if can_food.total_energy_kcal and can_food.total_energy_kcal > 0:
        can_food.protein_met_energy_pct = (can_food.protein_kcal / can_food.total_energy_kcal) * 100
        can_food.fat_met_energy_pct = (can_food.fat_kcal / can_food.total_energy_kcal) * 100
        can_food.carb_met_energy_pct = (can_food.carb_kcal / can_food.total_energy_kcal) * 100
    
    # 计算每1000kcal的营养素含量（营养密度指标）
    if can_food.total_energy_kcal and can_food.total_energy_kcal > 0:
        # 能量单位是kcal/100g，换算成kcal/kg需要*10
        energy_per_kg = can_food.total_energy_kcal * 10  # kcal/kg
        factor = 1000 / energy_per_kg if energy_per_kg > 0 else 0
        if can_food.calcium_wet is not None:
            can_food.calcium_per_1000kal = can_food.calcium_wet * factor
        if can_food.phosphorus_wet is not None:
            can_food.phosphorus_per_1000kal = can_food.phosphorus_wet * factor
    
    # 计算磷含量指标（高磷/中磷/低磷）
    if can_food.phosphorus_per_1000kal is not None:
        if can_food.phosphorus_per_1000kal > 2400:
            can_food.phosphorus_level = '高磷'
        elif can_food.phosphorus_per_1000kal < 1800:
            can_food.phosphorus_level = '低磷'
        else:
            can_food.phosphorus_level = '中磷'
    
    # 计算蛋白质/脂肪比值
    if can_food.protein is not None and can_food.fat is not None and can_food.fat > 0:
        can_food.protein_fat_ratio = can_food.protein / can_food.fat
    
    # 根据标准判断合格
    def check_pass(field_value, standard):
        if field_value is None or standard is None:
            return None
        threshold = standard.threshold
        threshold_max = getattr(standard, 'threshold_max', None)
        
        if standard.operator == '>=':
            return '合格' if field_value >= threshold else '不合格'
        elif standard.operator == '<=':
            return '合格' if field_value <= threshold else '不合格'
        elif standard.operator == '>':
            return '合格' if field_value > threshold else '不合格'
        elif standard.operator == '<':
            return '合格' if field_value < threshold else '不合格'
        elif standard.operator == 'range':
            if threshold_max is None:
                return None
            return '合格' if threshold <= field_value <= threshold_max else '不合格'
        return None
    
    # 蛋白合格判定
    if 'protein' in standards_map:
        can_food.protein_pass = check_pass(can_food.protein, standards_map['protein'])
    
    # 脂肪合格判定
    if 'fat' in standards_map:
        can_food.fat_pass = check_pass(can_food.fat, standards_map['fat'])
    
    # 纤维合格判定
    if 'fiber' in standards_map:
        can_food.fiber_pass = check_pass(can_food.fiber, standards_map['fiber'])
    
    # 灰分合格判定
    if 'ash' in standards_map:
        can_food.ash_pass = check_pass(can_food.ash, standards_map['ash'])
    
    # 水分合格判定
    if 'moisture' in standards_map:
        can_food.moisture_pass = check_pass(can_food.moisture, standards_map['moisture'])
    
    # 钙磷比合格判定
    if 'ca_ph_ratio' in standards_map and can_food.ca_ph_ratio is not None:
        can_food.ca_ph_pass = check_pass(can_food.ca_ph_ratio, standards_map['ca_ph_ratio'])
    
    return can_food
