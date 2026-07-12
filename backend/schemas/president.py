from pydantic import BaseModel
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

	class Config:
		from_attributes = True


class President(PresidentBase):
	id: int

	class Config:
		from_attributes = True
