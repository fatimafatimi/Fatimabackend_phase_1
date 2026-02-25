from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,  nullable=False)
    email = Column(String, unique= True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column (String, default ="user")
    projects = relationship("Project", back_populates="owner")
    
    
#  ForeignKey → database enforcement
#  relationship → ORM navigation
#  back_populates → two-way connection
#  nullable=False → strict integrity
#  Ownership architecture