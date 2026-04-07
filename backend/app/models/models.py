from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Brand(Base):
    __tablename__ = "brands"

    code = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    country = Column(String(20), default='国内')  # 国内 / 国外
    created_date = Column(Text, nullable=True)

    flavors = relationship("Flavor", back_populates="brand")


class Flavor(Base):
    __tablename__ = "flavors"

    code = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    brand_code = Column(Integer, ForeignKey("brands.code"), nullable=False)
    photo = Column(Text, nullable=True)
    creator = Column(String(50), nullable=True)
    created_date = Column(Text, nullable=True)

    brand = relationship("Brand", back_populates="flavors")
    cans = relationship("CanFood", back_populates="flavor")


class CanFood(Base):
    __tablename__ = "can_foods"

    code = Column(Integer, primary_key=True, index=True)
    brand_code = Column(Integer, ForeignKey("brands.code"), nullable=False)
    flavor_code = Column(Integer, ForeignKey("flavors.code"), nullable=True)
    description = Column(Text, nullable=True)

    protein = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    ash = Column(Float, nullable=True)
    fiber = Column(Float, nullable=True)
    moisture = Column(Float, nullable=True)
    calcium_wet = Column(Float, nullable=True)
    phosphorus_wet = Column(Float, nullable=True)
    nfe_wet = Column(Float, nullable=True)
    ca_ph_ratio = Column(Float, nullable=True)
    calcium_dm = Column(Float, nullable=True)
    phosphorus_dm = Column(Float, nullable=True)
    calcium_per_1000kal = Column(Float, nullable=True)
    phosphorus_per_1000kal = Column(Float, nullable=True)
    phosphorus_level = Column(Text, nullable=True)
    nfe_dm = Column(Float, nullable=True)
    protein_dm = Column(Float, nullable=True)
    fat_dm = Column(Float, nullable=True)
    ash_dm = Column(Float, nullable=True)
    carb_met_energy_pct = Column(Float, nullable=True)
    protein_met_energy_pct = Column(Float, nullable=True)
    fat_met_energy_pct = Column(Float, nullable=True)
    total_energy_kcal = Column(Float, nullable=True)
    carb_kcal = Column(Float, nullable=True)
    protein_kcal = Column(Float, nullable=True)
    fat_kcal = Column(Float, nullable=True)
    labeled_kcal = Column(Float, nullable=True)

    protein_pass = Column(Text, nullable=True)
    fat_pass = Column(Text, nullable=True)
    fiber_pass = Column(Text, nullable=True)
    ash_pass = Column(Text, nullable=True)
    moisture_pass = Column(Text, nullable=True)
    ca_ph_pass = Column(Text, nullable=True)
    protein_fat_ratio = Column(Float, nullable=True)
    protein_level = Column(Text, nullable=True)

    creator = Column(String(50), nullable=True)
    created_date = Column(Text, nullable=True)
    photo = Column(Text, nullable=True)

    brand = relationship("Brand")
    flavor = relationship("Flavor", back_populates="cans")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), default='user')
    status = Column(String(20), default='active')
    created_date = Column(Text, nullable=True)


class Standard(Base):
    __tablename__ = "standards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    field = Column(String(50), nullable=False)
    operator = Column(String(10), nullable=False)
    threshold = Column(Float, nullable=True)
    threshold_max = Column(Float, nullable=True)
    unit = Column(String(20), nullable=True)
    status = Column(String(20), default='active')
    created_date = Column(Text, nullable=True)
