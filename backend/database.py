from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "sqlite:///./test.db"
# db_url = "postgresql://postgres:PassedtheWord@localhost:5432/testdb"

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

  