from pydantic import BaseModel, ConfigDict
from typing import Optional


class SeasonBase(BaseModel):
    name: str
    is_active: Optional[bool] = True


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class Season(SeasonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)