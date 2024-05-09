from fastapi import FastAPI
from enum import Enum


class CompanyFilters(str, Enum):
    COMPANY_NAME = "company_name"
    WEBSITE = "website"
    COUNTRY = "country"


class FilterTypeEnum(str, Enum):
    EXACT = "exact"
    FUZZY = "fuzzy"



