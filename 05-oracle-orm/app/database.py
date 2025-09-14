from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from .config import settings

# SQLAlchemy uses a URL. For python-oracledb use dialect "oracle+oracledb"
# Example: oracle+oracledb://user:pass@host:port/?service_name=MYDB
user = settings.ORACLE_USER
password = quote_plus(settings.ORACLE_PASSWORD)
host = settings.ORACLE_HOST
port = settings.ORACLE_PORT
service = settings.ORACLE_SERVICE

# Correct dialect for SQLAlchemy 1.4.23
DATABASE_URL = (
    f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service}"
)

# Create synchronous engine
engine = create_engine(
    DATABASE_URL,
    echo=settings.SQL_ECHO,
)

# Create the session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()