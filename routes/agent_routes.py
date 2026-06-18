from fastapi import APIRouter, HTTPException, status
from utils.models import CreateAgent, UpdateAgent
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
        raise
    

@router.get("/agents")
def all_agents():
    try:
        return agent.get_all_agents()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect the server."
        )
    

@router.get("/agents/{a_id}")
def get_agent_by_id(a_id: int):
    try:
        if type(a_id) != int:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        data = agent.get_agent_by_id(a_id)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID not exist."
            )
    except Exception:
        raise


@router.put("/agents/{a_id}")
def update_agent(a_id: int, data: UpdateAgent):
    try:
        if type(a_id) != int:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        
        exist_id = agent.get_agent_by_id(a_id)
        if exist_id is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ID not fount."
                )
        
        data_dict = data.model_dump(exclude_unset=True)
        if not data_dict:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="empty data"
            )
        
        success = agent.update_agent(a_id, data_dict)
        if success:
            return {"message": f"agent {a_id} updated."}
        return {"message": f"agent {a_id} not updated."}
    
    except Exception:
        raise



@router.put("/agents/{a_id}/deactivate")
def deactivate_agent(a_id: int):
    try:
        if type(a_id) != int:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        
        exist_id = agent.get_agent_by_id(a_id)
        if exist_id is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ID not fount."
                )
        return agent.deactivate_agent(a_id)
    
    except Exception:
        raise


@router.get("/agents/{a_id}/performance")
def agent_report(a_id: int):
    try:
        if type(a_id) != int:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        
        exist_id = agent.get_agent_by_id(a_id)
        if exist_id is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ID not fount."
                )
        return agent.get_agent_performance(a_id)
    
    except Exception:
        raise
