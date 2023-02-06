from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

# inspector = inspect(engine)

# for table_name in inspector.get_table_names():
#     columns = inspector.get_columns(table_name)
#     print("Table: ", table_name)
#     for column in columns:
#         print("Column: ", column['name'])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()