from pydantic import BaseModel
from typing import Optional, List


# Brand Schemas
class BrandBase(BaseModel):
    alias: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    name: str
    created_date: Optional[str] = None


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    alias: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    name: Optional[str] = None
    created_date: Optional[str] = None


class Brand(BrandBase):
    code: int

    class Config:
        from_attributes = True


# Flavor Schemas
class FlavorBase(BaseModel):
    name: str
    brand_code: int
    photo: Optional[str] = None
    creator: Optional[str] = None
    created_date: Optional[str] = None


class FlavorCreate(FlavorBase):
    pass


class FlavorUpdate(BaseModel):
    name: Optional[str] = None
    brand_code: Optional[int] = None
    photo: Optional[str] = None
    creator: Optional[str] = None
    created_date: Optional[str] = None


class Flavor(FlavorBase):
    code: int
    brand: Optional[Brand] = None

    class Config:
        from_attributes = True


# CanFood Schemas
class CanFoodBase(BaseModel):
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


class CanFood(CanFoodBase):
    code: int
    brand: Optional[Brand] = None
    flavor: Optional[Flavor] = None

    class Config:
        from_attributes = True


# Query Schemas
class CanFoodQuery(BaseModel):
    brand_code: Optional[int] = None
    flavor_code: Optional[int] = None
    description: Optional[str] = None
    min_protein: Optional[float] = None
    max_protein: Optional[float] = None
    min_fat: Optional[float] = None
    max_fat: Optional[float] = None
    protein_pass: Optional[str] = None
    page: int = 1
    page_size: int = 20
