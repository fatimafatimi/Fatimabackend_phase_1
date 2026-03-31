# models/tenant.py
from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
    users = relationship("User", back_populates="tenant")
    roles = relationship("Role", back_populates="tenant")

    permissions = relationship("Permission", back_populates="tenant")
    projects = relationship("Project", back_populates="tenant")