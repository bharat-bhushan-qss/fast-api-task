from typing import List
from fastapi import HTTPException, APIRouter, Depends, Query
from src.models.companies import CompanyOut
from src.db.postgres_manager import get_db
from src.api.crud.companies import fetch_companies
from src.exceptions.common import NotFoundException
from src.constants import CompanyFilters, FilterTypeEnum
from src.api.crud.auth import get_current_user


v1_company_router = APIRouter()


@v1_company_router.get("/companies/", response_model=CompanyOut)
async def get_companies(filter_text: str = None, 
                        filter_type: FilterTypeEnum = "exact", 
                        filter_name: List[CompanyFilters] = Query(None), 
                        db = Depends(get_db), 
                        current_user = Depends(get_current_user)):
    try:
        companies = await fetch_companies(db, filter_type, filter_text, filter_name)
        if not companies:
            raise NotFoundException('No records found for the provided filter.')
        return {
            "data": companies
            }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
