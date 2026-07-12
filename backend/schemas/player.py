from pydantic import BaseModel, ConfigDict
from typing import Optional

class PlayerBase(BaseModel):
    name: str
    position: str
    age: int
    salary: int
    main_foot: str
    team_id: Optional[int] = None 

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    name: Optional[str] = None
    position: Optional[str] = None
    age: Optional[int] = None
    salary: Optional[int] = None
    main_foot: Optional[str] = None
    team_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
        
class Player(PlayerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)