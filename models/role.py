# models/role.py
from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

# Association table
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)

    # Relationships
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", back_populates="role")
    tenant = relationship("Tenant", back_populates="roles")

    # Multi-tenant uniqueness
    __table_args__ = (
        UniqueConstraint("name", "tenant_id", name="unique_role_per_tenant"),
    )