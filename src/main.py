from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from src.api.v1.companies import v1_company_router
from src.api.v1.contacts import v1_contact_router
from src.api.v1.setup import v1_setup_router
from src.api.v1.auth import v1_auth_router
from src.db.postgres_manager import get_db
from src.exceptions.common import NotFoundException, ValidationException, UnauthorizedException


PROJECT_NAME = "Task Fast API" 

app = FastAPI(title=PROJECT_NAME)


# API documentation access on /docs
@app.get("/openapi.json")
async def get_openapi():
    return get_openapi(
        title="Task FAST API",
        version="1.0.0",
        description="API Documentation",
        routes=app.routes,
    )

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


@app.get("/")
async def read_root():
    return {"message": "Hello from Version 1 of APIs"}


API_PREFIX = ''

# fro setup
app.include_router(v1_setup_router, prefix=API_PREFIX, tags=['setup'],
                   dependencies=[Depends(get_db)])

# api urls
app.include_router(v1_company_router, prefix=API_PREFIX, tags=['company'],
                   dependencies=[Depends(get_db)])
app.include_router(v1_contact_router, prefix=API_PREFIX, tags=['contact'],
                   dependencies=[Depends(get_db)])
app.include_router(v1_auth_router, prefix=API_PREFIX, tags=['auth'],
                   dependencies=[Depends(get_db)])
