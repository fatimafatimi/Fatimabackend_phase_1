from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    projects = relationship("Project", back_populates="owner")

    role_id = Column(ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users")