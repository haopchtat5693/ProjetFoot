from pydantic import BaseModel, ConfigDict
from typing import Optional


class StadiumBase(BaseModel):
	name: str
	location: str
	capacity: int


class StadiumCreate(StadiumBase):
	pass


class StadiumUpdate(BaseModel):
	name: Optional[str] = None
	location: Optional[str] = None
	capacity: Optional[int] = None

	model_config = ConfigDict(from_attributes=True)


class Stadium(StadiumBase):
	id: int

	model_config = ConfigDict(from_attributes=True)
