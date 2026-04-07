#!/usr/bin/env python3
"""初始化数据库脚本"""

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
            Brand(name="味好美", country="中国", description="国内知名罐头品牌"),
            Brand(name="梅林", country="中国", description="上海老字号罐头品牌"),
            Brand(name="甘竹", country="中国", description="广东地区知名罐头品牌"),
            Brand(name="史云生", country="中国香港", description="香港知名罐头品牌"),
        ]
        db.add_all(brands)
        db.commit()
        
        for brand in brands:
            db.refresh(brand)
        print(f"已插入 {len(brands)} 个品牌")

        # 插入样本口味
        flavors = [
            Flavor(name="红烧猪肉", brand_id=brands[0].id, description="经典红烧口味"),
            Flavor(name="清蒸猪肉", brand_id=brands[0].id, description="清淡蒸制口味"),
            Flavor(name="午餐肉", brand_id=brands[1].id, description="经典午餐肉罐头"),
            Flavor(name="番茄沙司", brand_id=brands[2].id, description="番茄酱汁"),
            Flavor(name="鲜玉米", brand_id=brands[2].id, description="甜玉米罐头"),
            Flavor(name="浓汤", brand_id=brands[3].id, description="浓郁汤品"),
        ]
        db.add_all(flavors)
        db.commit()
        
        for flavor in flavors:
            db.refresh(flavor)
        print(f"已插入 {len(flavors)} 个口味")

        # 插入样本罐头
        cans = [
            CanFood(
                name="红烧猪肉罐头420g", flavor_id=flavors[0].id, barcode="6901234567890",
                calories=250, protein=15.5, fat=18.2, carbohydrate=5.3, moisture=58.0,
                phosphorus=120, calcium=45, net_weight=420, drained_weight=250,
                is_quality_passed=True, quality_notes="各项指标合格",
                description="精选猪肉，古法红烧，口感鲜嫩"
            ),
            CanFood(
                name="清蒸猪肉罐头340g", flavor_id=flavors[1].id, barcode="6901234567891",
                calories=180, protein=20.1, fat=10.5, carbohydrate=2.1, moisture=65.0,
                phosphorus=150, calcium=35, net_weight=340, drained_weight=200,
                is_quality_passed=True, quality_notes="合格",
                description="清淡蒸制，保留猪肉原味"
            ),
            CanFood(
                name="午餐肉罐头340g", flavor_id=flavors[2].id, barcode="6901234567892",
                calories=290, protein=12.0, fat=25.0, carbohydrate=2.0, moisture=55.0,
                phosphorus=100, calcium=30, net_weight=340, drained_weight=220,
                is_quality_passed=True, quality_notes="符合国家标准",
                description="经典午餐肉，可煎可炒可火锅"
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
