from fastapi import FastAPI, Depends
from src.api.v1.companies import v1_company_router
from src.api.v1.contacts import v1_contact_router
from src.api.v1.setup import v1_setup_router
from src.db.postgres_manager import get_db
from src.exceptions.common import NotFoundException, ValidationException, UnauthorizedException
from fastapi.responses import JSONResponse


PROJECT_NAME = "Task Fast API" 

app = FastAPI(title=PROJECT_NAME)


# Define exception handlers
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

@app.exception_handler(ValidationException)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


API_PREFIX = '/api/v1'

# fro setup
app.include_router(v1_setup_router, prefix=API_PREFIX, tags=['setup'],
                   dependencies=[Depends(get_db)])

# api urls
app.include_router(v1_company_router, prefix=API_PREFIX, tags=['company'],
                   dependencies=[Depends(get_db)])
app.include_router(v1_contact_router, prefix=API_PREFIX, tags=['contact'],
                   dependencies=[Depends(get_db)])

