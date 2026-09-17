import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "epicevents.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"


engine = create_engine(DATABASE_URL, echo=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)