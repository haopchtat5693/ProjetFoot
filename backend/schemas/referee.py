from pydantic import BaseModel, ConfigDict
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

	model_config = ConfigDict(from_attributes=True)


class Referee(RefereeBase):
	id: int

	model_config = ConfigDict(from_attributes=True)
