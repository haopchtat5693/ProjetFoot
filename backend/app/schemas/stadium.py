from pydantic import BaseModel, ConfigDict
from typing import Optional


class StadiumBase(BaseModel):
	name: str
	city: str
	address: str
	capacity: int


class StadiumCreate(StadiumBase):
	pass


class StadiumUpdate(BaseModel):
	name: Optional[str] = None
	city: Optional[str] = None
	address: Optional[str] = None
	capacity: Optional[int] = None

	model_config = ConfigDict(from_attributes=True)


class Stadium(StadiumBase):
	id: int

	model_config = ConfigDict(from_attributes=True)
