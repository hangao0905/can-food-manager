from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.models import Brand as BrandModel, Flavor as FlavorModel, CanFood as CanFoodModel, User as UserModel
from app.routers.auth import get_current_user

router = APIRouter(prefix="/stats", tags=["数据统计"])

@router.get("/")
def get_stats(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # 品牌统计
    total_brands = db.query(BrandModel).count()
    domestic_brands = db.query(BrandModel).filter(BrandModel.country == '国内').count()
    foreign_brands = db.query(BrandModel).filter(BrandModel.country == '国外').count()

    # 口味统计（按口味所属品牌的国家）
    total_flavors = db.query(FlavorModel).count()
    domestic_flavors = db.query(FlavorModel).join(BrandModel, FlavorModel.brand_code == BrandModel.code).filter(BrandModel.country == '国内').count()
    foreign_flavors = db.query(FlavorModel).join(BrandModel, FlavorModel.brand_code == BrandModel.code).filter(BrandModel.country == '国外').count()

    # 罐头统计
    total_cans = db.query(CanFoodModel).count()

    # 用户统计
    total_users = db.query(UserModel).count()

    # 合格指标统计（随机抽取前100条）
    cans_sample = db.query(CanFoodModel).limit(100).all()
    protein_pass = sum(1 for c in cans_sample if c.protein_pass == '合格')
    fat_pass = sum(1 for c in cans_sample if c.fat_pass == '合格')
    ash_pass = sum(1 for c in cans_sample if c.ash_pass == '合格')

    return {
        "brands": {"total": total_brands, "domestic": domestic_brands, "foreign": foreign_brands},
        "flavors": {"total": total_flavors, "domestic": domestic_flavors, "foreign": foreign_flavors},
        "cans": {"total": total_cans},
        "users": {"total": total_users},
        "qualification": {
            "protein_pass_rate": round(protein_pass, 1) if cans_sample else 0,
            "fat_pass_rate": round(fat_pass, 1) if cans_sample else 0,
            "ash_pass_rate": round(ash_pass, 1) if cans_sample else 0,
            "sample_count": len(cans_sample),
        }
    }
