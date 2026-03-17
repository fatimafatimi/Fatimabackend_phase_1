from database import Base, engine  # your SQLAlchemy Base and engine
from models.user import User
from models.project import Project
from models.task import Task

# Create all tables defined in your models
Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully")
