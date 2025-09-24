import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    notification_preferences = Column(JSON, default={"email": True, "push": False})
    stripe_customer_id = Column(String, unique=True, nullable=True)

    addresses = relationship("Address", back_populates="owner", cascade="all, delete-orphan")

class Address(Base):
    __tablename__ = "addresses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    street_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    source_config = Column(JSON, nullable=True) # e.g., {"county_assessor": "active"}

    owner = relationship("User", back_populates="addresses")
    records = relationship("Record", back_populates="address", cascade="all, delete-orphan")

class Record(Base):
    __tablename__ = "records"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    source = Column(String, nullable=False, index=True) # e.g., "county_assessor_xyz"
    record_type = Column(String, nullable=False, index=True) # e.g., "Permit", "Lien"
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    url = Column(String, nullable=True)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)

    address = relationship("Address", back_populates="records")
