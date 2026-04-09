from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BrandBase(BaseModel):
    name: str
    created_date: Optional[str] = None
    alias: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BaseModel):
    name: Optional[str] = None
    created_date: Optional[str] = None
    alias: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None

class Brand(BrandBase):
    code: int

    class Config:
        from_attributes = True
