from src.config.database import engine
from src.models.base import Base

from src.models.user import User
from src.models.client import Client

print("Creation des tables dans la base SQLite...")
Base.metadata.create_all(bind=engine)
print("Tables creees avec succes !")