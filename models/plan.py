from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from database import Base  
from sqlalchemy.orm import relationship

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # safer for money
    billing_cycle = Column(String, nullable=False)
    stripe_price_id = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    subscriptions = relationship("Subscription", back_populates="plan")

    def __repr__(self):
        return f"<Plan {self.name} - {self.billing_cycle} - ${self.price}>"