from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Database URL
database_url = "postgresql://postgres:Blake3214@localhost/neobond"

# Create a new SQLAlchemy engine
engine = create_engine(database_url)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models
Base = declarative_base()

# Dependency to get the database session
# This function will be used to inject a database session into path operations

def get_db():
  db = SessionLocal()
  try:
    print("Get DB Session Called Successfully")
    yield db
  finally:
    db.close()
