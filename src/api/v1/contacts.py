from typing import List
from fastapi import HTTPException, APIRouter, Depends, Query
from src.models.contacts import ContactOut
from src.db.postgres_manager import get_db
from src.api.crud.contacts import fetch_contacts
from src.exceptions.common import NotFoundException
from src.api.crud.auth import get_current_user 


v1_contact_router = APIRouter()


@v1_contact_router.get("/contacts/", response_model=ContactOut)
async def get_contacts(job_title: str = None, 
                       job_level: str = None, 
                       job_function: str = None, 
                       limit: int = None, 
                       db=Depends(get_db),
                       current_user = Depends(get_current_user)):
    try:
        contacts = await fetch_contacts(db, job_title, job_level, job_function, limit)
        if not contacts:
            raise NotFoundException('No records found for the provided filter.')
        
        return {
            "data": contacts
            }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
