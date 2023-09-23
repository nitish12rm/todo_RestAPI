from pydantic import BaseModel,EmailStr,conint
from typing import Optional

class UserCreate(BaseModel):
    name:str
    email: EmailStr
    password: str
class UserOut(BaseModel):
    id:int
    name:str
    email: EmailStr
    
    class Config:
        form_attributes = True
