from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.role import role_permissions  # this is okay

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")