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
    name:str | None = None
    specialty:str | None = None
    is_active:bool | None = None
    completed_missions:int | None = None
    failed_missions:int | None = None
    agent_rank:Literal["Junior", "Senior", "Commander"] | None = None


class CreateMission(BaseModel):
    title:str
    description:str
    location:str
    difficulty:int
    importance:int
    status:Literal['NEW', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETE', 'FAILED', 'CANCELLED']
    assigned_agent_id:int | None = None

class UpdateMission(BaseModel):
    pass