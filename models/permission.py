from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.role import role_permissions

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")