from pydantic import BaseModel
from typing import List
from src.models.companies import CompanyBase
from src.models.common import BaseCommonFields 


class Contact(BaseCommonFields):
    company_id: int
    contact_name: str
    job_title: str
    job_level: str
    job_function: str


class ContactBaseOut(Contact):
    company: CompanyBase


class ContactOut(BaseModel):
    data: List[ContactBaseOut]
