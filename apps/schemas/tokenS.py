from pydantic import BaseModel,EmailStr,conint
from typing import Optional
class token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id:Optional[int] = None