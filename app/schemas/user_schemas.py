from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from uuid import UUID
import datetime

# --- Base Schemas for reusability ---
class OrmBase(BaseModel):
    class Config:
        orm_mode = True

# --- User Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(OrmBase):
    id: UUID
    email: EmailStr
    created_at: datetime.datetime
    stripe_customer_id: Optional[str] = None

# --- Address Schemas ---
class AddressCreate(BaseModel):
    street_address: str
    city: str
    state: str
    zip_code: str
    source_config: Optional[Dict[str, Any]] = None

class Address(OrmBase):
    id: UUID
    user_id: UUID
    street_address: str
    city: str
    state: str
    zip_code: str

# --- Record Schemas ---
class Record(OrmBase):
    id: UUID
    address_id: UUID
    source: str
    record_type: str
    title: str
    summary: Optional[str] = None
    url: Optional[str] = None
    scraped_at: datetime.datetime
