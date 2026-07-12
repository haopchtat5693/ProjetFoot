from pydantic import BaseModel, ConfigDict
from typing import Optional


class CoachBase(BaseModel):
	name: str
	age: int
	salary: int


class CoachCreate(CoachBase):
	pass


class CoachUpdate(BaseModel):
	name: Optional[str] = None
	age: Optional[int] = None
	salary: Optional[int] = None

	model_config = ConfigDict(from_attributes=True)


class Coach(CoachBase):
	id: int

	model_config = ConfigDict(from_attributes=True)
