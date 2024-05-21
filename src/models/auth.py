from pydantic import BaseModel
from typing import List, Optional
from src.models.common import BaseCommonFields


# User model
class UserBase(BaseModel):
    username: str
    password: str


class User(BaseCommonFields, UserBase):
    pass


class UserOut(BaseModel):
    access_token: Optional[str] = ""

