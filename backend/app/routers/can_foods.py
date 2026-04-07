from fastapi import APIRouter, Depends, HTTPException
import datetime
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.models import CanFood as CanFoodModel, Standard as StandardModel
from app.routers.auth import get_current_user

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


class CanFoodCreate(BaseModel):
    brand_code: int
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
    labeled_kcal: Optional[float] = None
    photo: Optional[str] = None


def _apply_standard(value: float, operator: str, threshold: float, threshold_max: float = None) -> bool:
    if value is None:
        return False
    if operator == '>=': return value >= threshold
    if operator == '<=': return value <= threshold
    if operator == '>':  return value > threshold
    if operator == '<':  return value < threshold
    if operator == 'range': return value >= threshold and value <= threshold_max
    return False


def _calc_nutrients(data: dict, db=None) -> dict:
    """根据输入的营养成分自动计算派生字段"""
    protein  = data.get('protein')
    fat     = data.get('fat')
    ash     = data.get('ash')
    fiber   = data.get('fiber')
    moisture= data.get('moisture')
    calcium_wet  = data.get('calcium_wet')
    phosphorus_wet = data.get('phosphorus_wet')
    nfe_wet = data.get('nfe_wet')

    dry_matter = (1 - moisture) if moisture is not None else None

    # 干物质换算
    if dry_matter and dry_matter > 0:
        if protein is not None:       data['protein_dm']       = protein / dry_matter
        if fat is not None:           data['fat_dm']           = fat / dry_matter
        if ash is not None:           data['ash_dm']           = ash / dry_matter
        if nfe_wet is not None:      data['nfe_dm']           = nfe_wet / dry_matter
        if calcium_wet is not None:  data['calcium_dm']       = calcium_wet / dry_matter
        if phosphorus_wet is not None: data['phosphorus_dm']  = phosphorus_wet / dry_matter
    else:
        data['protein_dm'] = data['fat_dm'] = data['ash_dm'] = data['nfe_dm'] = None
        data['calcium_dm'] = data['phosphorus_dm'] = None

    # 代谢能 (kcal/100g 湿基，再换算 kcal/kg)
    # 蛋白 3.5, 脂肪 8.5, 碳水 3.5
    kcal_100g = 0.0
    p_kcal = (protein * 3.5 * 100) if protein else 0.0
    f_kcal = (fat * 8.5 * 100) if fat else 0.0
    c_kcal = (nfe_wet * 3.5 * 100) if nfe_wet else 0.0
    kcal_100g = p_kcal + f_kcal + c_kcal

    if kcal_100g > 0:
        data['total_energy_kcal'] = kcal_100g * 10  # kcal/kg
        data['protein_kcal'] = p_kcal * 10
        data['fat_kcal']     = f_kcal * 10
        data['carb_kcal']    = c_kcal * 10
        data['protein_met_energy_pct'] = p_kcal / kcal_100g
        data['fat_met_energy_pct']     = f_kcal / kcal_100g
        data['carb_met_energy_pct']    = c_kcal / kcal_100g
    else:
        data['total_energy_kcal'] = data['protein_kcal'] = data['fat_kcal'] = data['carb_kcal'] = None
        data['protein_met_energy_pct'] = data['fat_met_energy_pct'] = data['carb_met_energy_pct'] = None

    # 钙磷比
    if phosphorus_wet and phosphorus_wet > 0 and calcium_wet:
        data['ca_ph_ratio'] = calcium_wet / phosphorus_wet

    # 钙/磷 mg/1000kcal
    total = data.get('total_energy_kcal')
    if total and total > 0:
        if calcium_wet is not None:
            data['calcium_per_1000kal'] = calcium_wet * 1000 * 10 / total
        if phosphorus_wet is not None:
            data['phosphorus_per_1000kal'] = phosphorus_wet * 1000 * 10 / total
            p_mg_kcal = data['phosphorus_per_1000kal']
            if p_mg_kcal > 2400:      data['phosphorus_level'] = '高磷'
            elif p_mg_kcal < 1800:    data['phosphorus_level'] = '低磷'
            else:                     data['phosphorus_level'] = '中磷'
    else:
        data['calcium_per_1000kal'] = data['phosphorus_per_1000kal'] = None

    # 蛋白质：脂肪比
    if fat and fat > 0 and protein:
        data['protein_fat_ratio'] = protein / fat
    else:
        data['protein_fat_ratio'] = None

    # 合格指标
    # 合格指标 - 从 DB standards 表读取规则
    if db is not None:
        standards = db.query(StandardModel).filter(StandardModel.status == 'active').all()
        pass_fields = {
            'protein': 'protein_pass', 'fat': 'fat_pass', 'fiber': 'fiber_pass',
            'ash': 'ash_pass', 'moisture': 'moisture_pass', 'ca_ph_ratio': 'ca_ph_pass'
        }
        for s in standards:
            val = data.get(s.field)
            if val is None:
                continue
            ok = _apply_standard(val, s.operator, s.threshold, s.threshold_max)
            if s.field in pass_fields:
                data[pass_fields[s.field]] = '合格' if ok else '不合格'
            # 磷含量指标
            if s.name == '磷含量指标-高' and s.operator == '>' and s.threshold == 2400:
                data['phosphorus_level'] = '高磷' if ok else None
            if s.name == '磷含量指标-低' and s.operator == '<' and s.threshold == 1800:
                data['phosphorus_level'] = '低磷' if ok else ('中磷' if data.get('phosphorus_per_1000kal') else None)
            # 蛋白质水平
            if s.name == '蛋白质:脂肪-优秀' and s.operator == '>' and s.threshold == 3.0:
                if ok: data['protein_level'] = '优秀'
            if s.name == '蛋白质:脂肪-一般' and s.operator == '>' and s.threshold == 1.5:
                if ok and data.get('protein_level') != '优秀': data['protein_level'] = '一般'
            if data.get('protein_fat_ratio') is not None and data.get('protein_level') is None:
                r = data['protein_fat_ratio']
                if r <= 1.5: data['protein_level'] = '不合格'
    else:
        # 回退：硬编码规则
        if protein is not None:
            data['protein_pass'] = '合格' if protein >= 0.1 else '不合格'
        if fat is not None:
            data['fat_pass'] = '合格' if fat <= 0.09 else '不合格'
        if fiber is not None:
            data['fiber_pass'] = '合格' if fiber <= 0.03 else '不合格'
        if ash is not None:
            data['ash_pass'] = '合格' if ash <= 0.02 else '不合格'
        if moisture is not None:
            data['moisture_pass'] = '合格' if moisture <= 0.8 else '不合格'
        if data.get('ca_ph_ratio') is not None:
            r = data['ca_ph_ratio']
            data['ca_ph_pass'] = '合格' if (r >= 1.1 and r <= 1.4) else '不合格'
        if data.get('protein_fat_ratio') is not None:
            r = data['protein_fat_ratio']
            if r > 3:     data['protein_level'] = '优秀'
            elif r > 1.5: data['protein_level'] = '一般'
            else:         data['protein_level'] = '不合格'

    return data


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


@router.post("/")
def create_can_food(data: CanFoodCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # 生成新 code（格式：yyyymmddnnn，如 20260407001）
    today = datetime.date.today().strftime('%Y%m%d')
    prefix = f"{today}%"
    last = db.query(CanFoodModel).filter(CanFoodModel.code.like(prefix)).order_by(CanFoodModel.code.desc()).first()
    if last:
        next_num = int(str(last.code)[-3:]) + 1
    else:
        next_num = 1
    new_code = int(f"{today}{next_num:03d}")

    # 计算派生营养字段（copy避免mutation）
    import copy
    input_dict = copy.deepcopy(data.dict(exclude_none=True))
    calc = _calc_nutrients(input_dict, db)
    # 分离输入字段和计算字段
    input_fields = {k: v for k, v in calc.items()
                    if k in ('protein','fat','ash','fiber','moisture',
                             'calcium_wet','phosphorus_wet','nfe_wet','labeled_kcal')}
    calc_only = {k: v for k, v in calc.items()
                 if k not in input_fields}
    db_obj = CanFoodModel(
        code=new_code,
        creator=current_user['username'],
        brand_code=data.brand_code,
        flavor_code=data.flavor_code,
        description=data.description,
        photo=data.photo,
        **input_fields,
        **calc_only
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    # 重新查询以获取关联的 brand 和 flavor
    c = db.query(CanFoodModel).options(joinedload(CanFoodModel.brand), joinedload(CanFoodModel.flavor)).filter(CanFoodModel.code == new_code).first()
    return to_dict(c)


def list_can_foods(page: int = 1, page_size: int = 50, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    query = db.query(CanFoodModel).options(joinedload(CanFoodModel.brand), joinedload(CanFoodModel.flavor))
    skip = (page - 1) * page_size
    return [to_dict(c) for c in query.offset(skip).limit(page_size).all()]

@router.get("/{code}")
def get_can_food(code: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    c = db.query(CanFoodModel).options(joinedload(CanFoodModel.brand), joinedload(CanFoodModel.flavor)).filter(CanFoodModel.code == code).first()
    if not c:
        return {"error": "not found"}
    return to_dict(c)

@router.put("/{code}")
def update_can_food(code: int, data: CanFoodUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    c = db.query(CanFoodModel).filter(CanFoodModel.code == code).first()
    if not c:
        raise HTTPException(status_code=404, detail="罐头不存在")

    # 只更新用户传入的非 None 字段
    update_dict = data.dict(exclude_unset=True)

    # 如果用户更新了湿基营养成分，自动重新计算派生字段
    nutrition_keys = {'protein','fat','ash','fiber','moisture','calcium_wet','phosphorus_wet','nfe_wet'}
    needs_recalc = bool(nutrition_keys & set(update_dict.keys()))

    for field, value in update_dict.items():
        setattr(c, field, value)

    if needs_recalc:
        raw = {f: getattr(c, f) for f in nutrition_keys}
        raw.update({k: getattr(c, k) for k in update_dict if k in nutrition_keys})
        computed = _calc_nutrients(raw, db=db)
        for k, v in computed.items():
            setattr(c, k, v)

    db.commit()
    db.refresh(c)
    return to_dict(c)

@router.post("/{code}/recalc")
def recalc_can_food(code: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """重新计算某条罐头的所有派生字段（干物质、代谢能、合格指标等）"""
    c = db.query(CanFoodModel).filter(CanFoodModel.code == code).first()
    if not c:
        raise HTTPException(status_code=404, detail="罐头不存在")
    raw = {
        'protein': c.protein, 'fat': c.fat, 'ash': c.ash, 'fiber': c.fiber,
        'moisture': c.moisture, 'calcium_wet': c.calcium_wet,
        'phosphorus_wet': c.phosphorus_wet, 'nfe_wet': c.nfe_wet
    }
    computed = _calc_nutrients(raw, db=db)
    calc_fields = ['protein_dm','fat_dm','ash_dm','nfe_dm','calcium_dm','phosphorus_dm',
                   'ca_ph_ratio','calcium_per_1000kal','phosphorus_per_1000kal',
                   'phosphorus_level','total_energy_kcal','protein_kcal','fat_kcal',
                   'carb_kcal','protein_met_energy_pct','fat_met_energy_pct',
                   'carb_met_energy_pct','protein_fat_ratio',
                   'protein_pass','fat_pass','fiber_pass','ash_pass',
                   'moisture_pass','ca_ph_pass','protein_level']
    for k in calc_fields:
        setattr(c, k, computed.get(k))
    db.commit()
    db.refresh(c)
    return to_dict(c)

@router.post("/recalc-all")
def recalc_all(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """重新计算所有罐头的派生字段"""
    count = 0
    for c in db.query(CanFoodModel).all():
        raw = {
            'protein': c.protein, 'fat': c.fat, 'ash': c.ash, 'fiber': c.fiber,
            'moisture': c.moisture, 'calcium_wet': c.calcium_wet,
            'phosphorus_wet': c.phosphorus_wet, 'nfe_wet': c.nfe_wet
        }
        computed = _calc_nutrients(raw, db=db)
        calc_fields = ['protein_dm','fat_dm','ash_dm','nfe_dm','calcium_dm','phosphorus_dm',
                       'ca_ph_ratio','calcium_per_1000kal','phosphorus_per_1000kal',
                       'phosphorus_level','total_energy_kcal','protein_kcal','fat_kcal',
                       'carb_kcal','protein_met_energy_pct','fat_met_energy_pct',
                       'carb_met_energy_pct','protein_fat_ratio',
                       'protein_pass','fat_pass','fiber_pass','ash_pass',
                       'moisture_pass','ca_ph_pass','protein_level']
        for k in calc_fields:
            setattr(c, k, computed.get(k))
        count += 1
    db.commit()
    return {"message": f"已重新计算 {count} 条记录"}

@router.delete("/{code}")
def delete_can_food(code: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    c = db.query(CanFoodModel).filter(CanFoodModel.code == code).first()
    if not c:
        raise HTTPException(status_code=404, detail="罐头不存在")
    db.delete(c)
    db.commit()
    return {"message": "删除成功"}
