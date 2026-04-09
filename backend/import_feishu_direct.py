#!/usr/bin/env python3
"""
直接从飞书API导入数据到罐头管理系统
"""

import json
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.models import CanFood, Brand, Flavor
from sqlalchemy.orm import Session
from sqlalchemy import and_

# 这里需要实际的飞书API数据
# 由于我们无法在服务器上直接调用飞书API，这里使用从客户端获取的数据
# 数据应该通过其他方式传递到服务器

def parse_feishu_data(feishu_records):
    """解析飞书数据，转换为数据库格式"""
    can_foods = []
    
    for record in feishu_records:
        fields = record.get('fields', {})
        
        # 提取基础信息
        code = fields.get('code', '').strip()
        if not code:
            continue
            
        # 品牌名称
        brand_name = fields.get('品牌', '').strip()
        if not brand_name:
            continue
            
        # 口味
        flavor_data = fields.get('口味', [])
        flavor_name = ''
        if flavor_data and isinstance(flavor_data, list):
            if isinstance(flavor_data[0], dict):
                flavor_name = flavor_data[0].get('text', '').strip()
            else:
                flavor_name = str(flavor_data[0]).strip()
        
        # 提取数值字段
        try:
            # 基础营养信息
            protein = float(fields.get('蛋白质含量', 0))
            fat = float(fields.get('脂肪含量', 0))
            fiber = float(fields.get('粗纤维含量', 0))
            ash = float(fields.get('粗灰分含量', 0))
            moisture = float(fields.get('水分含量', 0))
            ca_wet = float(fields.get('钙含量-湿基', 0))
            ph_wet = float(fields.get('磷含量-湿基', 0))
            ca_ph_ratio = float(fields.get('钙磷比', 0))
            
            # 新增字段
            ca_per_1000kal = None
            if '钙含量\nmg|1000kal' in fields:
                ca_per_1000kal = float(fields.get('钙含量\nmg|1000kal', 0))
            elif '钙含量mg/1000kal' in fields:
                ca_per_1000kal = float(fields.get('钙含量mg/1000kal', 0))
                
            ph_per_1000kal = float(fields.get('磷含量mg/1000kal', 0))
            
            # 蛋白质脂肪比
            protein_fat_ratio = float(fields.get('蛋白质：脂肪', 0))
            
            # 磷含量指标
            ph_level_data = fields.get('磷含量指标', {})
            ph_level = None
            if isinstance(ph_level_data, dict):
                values = ph_level_data.get('value', [])
                if values and isinstance(values, list):
                    if isinstance(values[0], dict):
                        ph_level = values[0].get('text', '').strip()
                    else:
                        ph_level = str(values[0]).strip()
            
            # 罐头简介
            intro_data = fields.get('罐头简介', [])
            intro = ''
            if intro_data and isinstance(intro_data, list):
                if isinstance(intro_data[0], dict):
                    intro = intro_data[0].get('text', '').strip()
                else:
                    intro = str(intro_data[0]).strip()
            
            # 创建罐头对象
            can_food = {
                'code': code,
                'brand_name': brand_name,
                'flavor_name': flavor_name,
                'protein': protein,
                'fat': fat,
                'fiber': fiber,
                'ash': ash,
                'moisture': moisture,
                'ca_wet': ca_wet,
                'ph_wet': ph_wet,
                'ca_ph_ratio': ca_ph_ratio,
                'ca_per_1000kal': ca_per_1000kal,
                'ph_per_1000kal': ph_per_1000kal,
                'ph_level': ph_level,
                'protein_fat_ratio': protein_fat_ratio,
                'intro': intro,
                'raw_data': json.dumps(fields, ensure_ascii=False)
            }
            
            can_foods.append(can_food)
            
        except (ValueError, TypeError) as e:
            print(f"解析记录 {code} 时出错: {e}")
            continue
    
    return can_foods

def get_or_create_brand(db: Session, brand_name: str):
    """获取或创建品牌"""
    brand = db.query(Brand).filter(Brand.name == brand_name).first()
    if not brand:
        brand = Brand(
            name=brand_name,
            alias=brand_name,
            description=f"{brand_name}品牌",
            country="德国",  # 默认德国，实际应根据数据调整
            created_date=datetime.now()
        )
        db.add(brand)
        db.commit()
        db.refresh(brand)
    return brand

def get_or_create_flavor(db: Session, flavor_name: str, brand_code: int):
    """获取或创建口味"""
    if not flavor_name:
        return None
        
    flavor = db.query(Flavor).filter(
        and_(Flavor.name == flavor_name, Flavor.brand_code == brand_code)
    ).first()
    
    if not flavor:
        flavor = Flavor(
            name=flavor_name,
            brand_code=brand_code,
            photo="",  # 默认空
            created_date=datetime.now()
        )
        db.add(flavor)
        db.commit()
        db.refresh(flavor)
    return flavor

def import_data(db: Session, can_foods_data):
    """导入数据到数据库"""
    imported_count = 0
    updated_count = 0
    skipped_count = 0
    
    for data in can_foods_data:
        try:
            # 检查是否已存在
            existing = db.query(CanFood).filter(CanFood.code == data['code']).first()
            
            # 获取或创建品牌
            brand = get_or_create_brand(db, data['brand_name'])
            
            # 获取或创建口味
            flavor = get_or_create_flavor(db, data['flavor_name'], brand.code)
            
            if existing:
                # 更新现有记录
                existing.brand_code = brand.code
                if flavor:
                    existing.flavor_code = flavor.code
                existing.protein = data['protein']
                existing.fat = data['fat']
                existing.fiber = data['fiber']
                existing.ash = data['ash']
                existing.moisture = data['moisture']
                existing.ca_wet = data['ca_wet']
                existing.ph_wet = data['ph_wet']
                existing.ca_ph_ratio = data['ca_ph_ratio']
                existing.ca_per_1000kal = data['ca_per_1000kal']
                existing.ph_per_1000kal = data['ph_per_1000kal']
                existing.ph_level = data['ph_level']
                existing.protein_fat_ratio = data['protein_fat_ratio']
                existing.intro = data['intro']
                existing.raw_data = data['raw_data']
                existing.updated_date = datetime.now()
                
                updated_count += 1
                print(f"✓ 更新记录: {data['code']} - {brand.name} - {data['flavor_name']}")
                
            else:
                # 创建新记录
                can_food = CanFood(
                    code=data['code'],
                    brand_code=brand.code,
                    flavor_code=flavor.code if flavor else None,
                    protein=data['protein'],
                    fat=data['fat'],
                    fiber=data['fiber'],
                    ash=data['ash'],
                    moisture=data['moisture'],
                    ca_wet=data['ca_wet'],
                    ph_wet=data['ph_wet'],
                    ca_ph_ratio=data['ca_ph_ratio'],
                    ca_per_1000kal=data['ca_per_1000kal'],
                    ph_per_1000kal=data['ph_per_1000kal'],
                    ph_level=data['ph_level'],
                    protein_fat_ratio=data['protein_fat_ratio'],
                    intro=data['intro'],
                    raw_data=data['raw_data'],
                    created_date=datetime.now(),
                    updated_date=datetime.now()
                )
                db.add(can_food)
                imported_count += 1
                print(f"✓ 导入记录: {data['code']} - {brand.name} - {data['flavor_name']}")
                
        except Exception as e:
            print(f"✗ 处理记录 {data['code']} 时出错: {e}")
            skipped_count += 1
            continue
    
    db.commit()
    
    return imported_count, updated_count, skipped_count

def main():
    """主函数"""
    print("开始导入飞书多维表格数据...")
    
    # 这里应该从API获取数据，但暂时使用硬编码的示例数据
    # 实际使用时应该从飞书API获取
    print("注意：需要实际的飞书API数据")
    print("请将飞书数据通过其他方式传递到服务器")
    
    # 示例数据（仅用于测试）
    sample_data = [
        {
            "fields": {
                "code": "20250404001",
                "品牌": "gussto",
                "口味": [{"text": "鸡肉"}],
                "水分含量": 0.8,
                "蛋白质含量": 0.108,
                "脂肪含量": 0.062,
                "粗纤维含量": 0.004,
                "粗灰分含量": 0.024,
                "钙含量-湿基": 0.0025,
                "磷含量-湿基": 0.0019,
                "钙磷比": 1.3157894736842106,
                "钙含量\nmg|1000kal": 2747.25274725274,
                "磷含量mg/1000kal": 2289.37728937728,
                "蛋白质：脂肪": 1.74,
                "磷含量指标": {"type": 1, "value": [{"text": "中磷"}]},
                "罐头简介": [{"text": "Gussto恶魔喵鸡肉口味..."}]
            }
        }
    ]
    
    # 解析数据
    print("解析飞书数据...")
    can_foods_data = parse_feishu_data(sample_data)
    print(f"成功解析 {len(can_foods_data)} 条记录")
    
    if not can_foods_data:
        print("没有可导入的数据")
        return
    
    # 连接数据库并导入
    db = SessionLocal()
    try:
        imported, updated, skipped = import_data(db, can_foods_data)
        
        print("\n" + "="*50)
        print("导入完成！")
        print(f"新增记录: {imported}")
        print(f"更新记录: {updated}")
        print(f"跳过记录: {skipped}")
        print(f"总计处理: {imported + updated + skipped}")
        print("="*50)
        
    except Exception as e:
        print(f"导入过程中出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()