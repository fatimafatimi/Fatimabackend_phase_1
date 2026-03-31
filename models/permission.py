# models/permission.py
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from models.role import role_permissions

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)
    tenant = relationship("Tenant", back_populates="permissions")

    __table_args__ = (
        UniqueConstraint("name", "tenant_id", name="unique_permission_per_tenant"),
    )