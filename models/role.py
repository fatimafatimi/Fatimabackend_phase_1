from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many between roles and permissions
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User",back_populates="role")

