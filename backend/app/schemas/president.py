from pydantic import BaseModel, ConfigDict
from typing import Optional


class PresidentBase(BaseModel):
	name: str
	age: int
	salary: int


class PresidentCreate(PresidentBase):
	pass


class PresidentUpdate(BaseModel):
	name: Optional[str] = None
	age: Optional[int] = None
	salary: Optional[int] = None

	model_config = ConfigDict(from_attributes=True)


class President(PresidentBase):
	id: int

	model_config = ConfigDict(from_attributes=True)
