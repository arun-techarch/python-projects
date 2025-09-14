from sqlalchemy import Column, Integer, String, Identity
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Identity(start=6, increment=1), primary_key=True)
    name = Column(String(200), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(200), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)

    def __repr__(self):
        return f"User: [id={self.id}, name={self.name}, age={self.age}, gender={self.gender}, phone={self.phone}, email={self.email}, city={self.city}, country={self.country}]"