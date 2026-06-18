from fastapi import APIRouter, HTTPException, status
from utils.models import CreateAgent
from database.agent_db import AgentDB
from pydantic import error_wrappers


router = APIRouter()

agent = AgentDB()


@router.post("/agents",
             status_code=status.HTTP_201_CREATED)
def new_agent(data: CreateAgent):
    try:
        if data.agent_rank not in ("Junior", "Senior", "Commander"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid rank"
            )
        return agent.create_agent(data)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect the server.")