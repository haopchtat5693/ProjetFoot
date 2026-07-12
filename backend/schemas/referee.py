from pydantic import BaseModel
from typing import Optional


class RefereeBase(BaseModel):
	name: str
	age: int
	salary: int


class RefereeCreate(RefereeBase):
	pass


class RefereeUpdate(BaseModel):
	name: Optional[str] = None
	age: Optional[int] = None
	salary: Optional[int] = None

	class Config:
		from_attributes = True


class Referee(RefereeBase):
	id: int

	class Config:
		from_attributes = True
