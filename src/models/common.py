from pydantic import BaseModel


class BaseCommonFields(BaseModel):
    id: int
