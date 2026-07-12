from pydantic import BaseModel
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

	class Config:
		from_attributes = True


class Stadium(StadiumBase):
	id: int

	class Config:
		from_attributes = True
