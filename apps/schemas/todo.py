from pydantic import BaseModel,EmailStr,conint
from typing import Optional
from . import users
class todoCreate(BaseModel):
    task:str
class todoOut(BaseModel):
    id:int
    owner_id:int
    task:str
    
    class Config:
        form_attributes = True