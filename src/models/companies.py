from pydantic import BaseModel
from typing import List
from src.models.common import BaseCommonFields


class CompanyBase(BaseModel):
    company_name: str
    website: str
    country: str


class Company(BaseCommonFields, CompanyBase):
    pass


class CompanyOut(BaseModel):
    data: List[Company]
