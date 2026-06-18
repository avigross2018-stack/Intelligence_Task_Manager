from fastapi import APIRouter, HTTPException, status
from utils.models import CreateAgent, UpdateAgent
from database.agent_db import AgentDB
from logger import get_logger


router = APIRouter()
agent = AgentDB()
logger = get_logger()


@router.post("/agents",
             status_code=status.HTTP_201_CREATED)
def new_agent(data: CreateAgent):
    try:
        logger.info("Start to create new agent.")
        if data.agent_rank not in ("Junior", "Senior", "Commander"):
            logger.error("Failed to create new agent, Invalid rank")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid rank"
            )
        logger.info("New agent created")
        return agent.create_agent(data)

    except Exception:
        logger.error("Failed to create new agent.")
        raise
    

@router.get("/agents")
def all_agents():
    logger.info("Start to show all agents")
    try:
        logger.info("Return all agents")
        return agent.get_all_agents()
    except Exception:
        logger.error("Failed to show all agents")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect the server."
        )
    

@router.get("/agents/{a_id}")
def get_agent_by_id(a_id: int):
    logger.info("Start to show agent by ID.")
    try:
        if type(a_id) != int:
            logger.error("Failed to show agent by ID, Invalid ID.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        data = agent.get_agent_by_id(a_id)
        if data is None:
            logger.error("Failed to show agent by ID, ID not exist.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID not exist."
            )
        logger.info("Showing agent by ID.")
        return data
    except Exception:
        logger.error("Failed to show agent by ID.")
        raise


@router.put("/agents/{a_id}")
def update_agent(a_id: int, data: UpdateAgent):
    logger.info("Start to update agent.")
    try:
        if type(a_id) != int:
            logger.error("Failed to update agent, invalid ID.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        
        exist_id = agent.get_agent_by_id(a_id)
        if exist_id is None:
            logger.error("Failed to update agent, ID not fount.")
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ID not fount."
                )
        
        data_dict = data.model_dump(exclude_unset=True)
        if not data_dict:
            logger.error("Failed to update agent, empty data")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="empty data"
            )
        
        success = agent.update_agent(a_id, data_dict)
        if success:
            logger.info("Agent updated.")
            return {"message": f"agent {a_id} updated."}
        return {"message": f"agent {a_id} not updated."}
    
    except Exception:
        logger.error("Failed to update agent.")
        raise



@router.put("/agents/{a_id}/deactivate")
def deactivate_agent(a_id: int):
    logger.info("Start to deactivate agent.")
    try:
        if type(a_id) != int:
            logger.error("Failed to deactivate agent, Invalid ID.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        
        exist_id = agent.get_agent_by_id(a_id)
        if exist_id is None:
            logger.error("Failed to deactivate agent, ID not fount.")
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ID not fount."
                )
        logger.info("Agent deactivate.")
        return agent.deactivate_agent(a_id)
    
    except Exception:
        logger.error("Failed to deactivate agent.")
        raise


@router.get("/agents/{a_id}/performance")
def agent_report(a_id: int):
    logger.info("Start agent report.")
    try:
        if type(a_id) != int:
            logger.error("Failed agent report, Invalid ID.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        
        exist_id = agent.get_agent_by_id(a_id)
        if exist_id is None:
            logger.error("Failed agent report, ID not fount.")
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ID not fount."
                )
        logger.info("Return agent report.")
        return agent.get_agent_performance(a_id)
    
    except Exception:
        logger.error("Failed agent report.")
        raise
