from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    age: Optional[int]
    gender: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    city: Optional[str]
    country: Optional[str]

class UserCreate(UserBase):
   pass

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: int

    class Config:
        #orm_mode = True
        from_attributes = True
