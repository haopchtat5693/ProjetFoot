from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CoachCareerTeam(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CoachCareer(BaseModel):
    team: CoachCareerTeam
    start: date
    end: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class CoachBase(BaseModel):
    name: str
    age: Optional[int] = None
    nationality: Optional[str] = None
    photo: Optional[str] = None


class CoachCreate(CoachBase):
    pass


class CoachUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    nationality: Optional[str] = None
    photo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Coach(CoachBase):
    id: int
    career: list[CoachCareer] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
