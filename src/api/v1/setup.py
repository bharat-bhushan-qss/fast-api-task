from fastapi import HTTPException, APIRouter, Depends
from src.db.postgres_manager import get_db
from src.api.crud.setup import do_setup


v1_setup_router = APIRouter()


@v1_setup_router.get("/setup/", response_model={})
async def setup(db=Depends(get_db)):
    try:
        await do_setup(db)
        return {
            "status": True
        }
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
