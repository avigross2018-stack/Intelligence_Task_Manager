from pydantic import BaseModel
from typing import Literal


class CreateAgent(BaseModel):
    name:str
    specialty:str
    is_active:bool = True
    completed_missions:int = 0
    failed_missions:int = 0
    agent_rank:Literal["Junior", "Senior", "Commander"]

class UpdateAgent(BaseModel):
    pass


class CreateMission(BaseModel):
    pass

class UpdateMission(BaseModel):
    pass