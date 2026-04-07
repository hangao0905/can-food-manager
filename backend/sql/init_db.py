#!/usr/bin/env python3
"""初始化数据库脚本 - 按 Excel 41列结构"""

import sys
sys.path.insert(0, '/app')

from app.database import engine, SessionLocal
from app.models.models import Base, Brand, Flavor, CanFood

def init_database():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功!")

    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(Brand).count() > 0:
            print("数据库已有数据，跳过初始化样本数据")
            return

        # 插入样本品牌
        brands = [
            Brand(code=1, name="gussto"),
            Brand(code=2, name="Catz Finefood"),
        ]
        db.add_all(brands)
        db.commit()
        print(f"已插入 {len(brands)} 个品牌")

        # 插入样本口味
        flavors = [
            Flavor(code=1, name="鸡肉", brand_code=1),
            Flavor(code=2, name="牛肉", brand_code=1),
        ]
        db.add_all(flavors)
        db.commit()
        print(f"已插入 {len(flavors)} 个口味")

        # 插入样本罐头（匹配41列结构）
        cans = [
            CanFood(
                code=20250404001,
                brand_code=1,
                flavor_code=1,
                description="Gussto恶魔喵鸡肉口味罐头",
                protein=0.108, fat=0.062, ash=0.024, fiber=0.004, moisture=0.8,
                calcium_wet=0.0025, phosphorus_wet=0.0019, nfe_wet=0.002,
                ca_ph_ratio=1.32,
                protein_pass="合格", fat_pass="合格", fiber_pass="合格",
                ash_pass="合格", moisture_pass="合格", ca_ph_pass="合格",
                protein_level="合格",
                creator="admin", created_date="2025-04-04"
            ),
        ]
        db.add_all(cans)
        db.commit()
        print(f"已插入 {len(cans)} 个罐头产品")

        print("\n数据库初始化完成!")

    finally:
        db.close()

if __name__ == "__main__":
    init_database()
