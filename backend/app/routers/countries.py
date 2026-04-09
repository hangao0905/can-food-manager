from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter(prefix="/countries", tags=["国家字典"])

class CountryCreate(BaseModel):
    code: str
    name: str
    name_en: Optional[str] = None

class CountryUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    name_en: Optional[str] = None

@router.get("/", response_model=List[dict])
def list_countries(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id, code, name, name_en FROM countries ORDER BY id")).fetchall()
    return [{"id": row[0], "code": row[1], "name": row[2], "name_en": row[3]} for row in result]

@router.get("/{country_id}", response_model=dict)
def get_country(country_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id, code, name, name_en FROM countries WHERE id = :id"), {"id": country_id}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="国家不存在")
    return {"id": result[0], "code": result[1], "name": result[2], "name_en": result[3]}

@router.post("/", response_model=dict)
def create_country(data: CountryCreate, db: Session = Depends(get_db)):
    # 检查是否已存在
    existing = db.execute(text("SELECT id FROM countries WHERE code = :code"), {"code": data.code}).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="国家代码已存在")
    
    # 插入新记录
    db.execute(
        text("INSERT INTO countries (code, name, name_en) VALUES (:code, :name, :name_en)"),
        {"code": data.code, "name": data.name, "name_en": data.name_en}
    )
    db.commit()
    
    # 获取新插入的ID
    new_id = db.execute(text("SELECT last_insert_rowid()")).fetchone()[0]
    return {"id": new_id, "code": data.code, "name": data.name, "name_en": data.name_en}

@router.put("/{country_id}", response_model=dict)
def update_country(country_id: int, data: CountryUpdate, db: Session = Depends(get_db)):
    # 检查是否存在
    existing = db.execute(text("SELECT id FROM countries WHERE id = :id"), {"id": country_id}).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="国家不存在")
    
    # 构建更新语句
    update_fields = []
    params = {"id": country_id}
    
    if data.code is not None:
        update_fields.append("code = :code")
        params["code"] = data.code
    
    if data.name is not None:
        update_fields.append("name = :name")
        params["name"] = data.name
    
    if data.name_en is not None:
        update_fields.append("name_en = :name_en")
        params["name_en"] = data.name_en
    
    if update_fields:
        update_sql = f"UPDATE countries SET {', '.join(update_fields)} WHERE id = :id"
        db.execute(text(update_sql), params)
        db.commit()
    
    # 返回更新后的数据
    result = db.execute(text("SELECT id, code, name, name_en FROM countries WHERE id = :id"), {"id": country_id}).fetchone()
    return {"id": result[0], "code": result[1], "name": result[2], "name_en": result[3]}

@router.delete("/{country_id}")
def delete_country(country_id: int, db: Session = Depends(get_db)):
    # 检查是否存在
    existing = db.execute(text("SELECT id FROM countries WHERE id = :id"), {"id": country_id}).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="国家不存在")
    
    # 检查是否有品牌关联
    brand_count = db.execute(text("SELECT COUNT(*) FROM brands WHERE country_id = :id"), {"id": country_id}).fetchone()[0]
    if brand_count > 0:
        raise HTTPException(status_code=400, detail=f"该国家下有{brand_count}个品牌，无法删除")
    
    # 删除
    db.execute(text("DELETE FROM countries WHERE id = :id"), {"id": country_id})
    db.commit()
    return {"message": "删除成功"}
