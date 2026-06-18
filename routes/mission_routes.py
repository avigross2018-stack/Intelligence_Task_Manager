from fastapi import APIRouter, HTTPException, status
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from utils.models import CreateMission
from logger import get_logger

router = APIRouter()

mission = MissionDB()
agent = AgentDB()
logger = get_logger()

@router.post("/missions",
             status_code=status.HTTP_201_CREATED)
def new_mission(data: CreateMission):
    logger.info("Start create new mission.")
    try:
        if data.status not in ('NEW', 'ASSIGNED', 'IN_PROGRESS', 
                               'COMPLETE', 'FAILED', 'CANCELLED'):
            logger.error("Failed to create new mission, Invalid status.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status"
            )

        if data.difficulty > 10 or data.difficulty < 1:
            logger.error("Failed to create new mission, Invalid difficulty (1-10)")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid difficulty (1-10)"
            )
        
        if data.importance > 10 or data.importance < 1:
            logger.error("Failed to create new mission, Invalid importance (1-10)")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid importance (1-10)"
            )
        
        logger.info("New mission created.")
        return mission.create_mission(data)
    
    except Exception:
        logger.error("Failed to create new mission.")
        raise


@router.get("/missions")
def all_missions():
    logger.info("Start show all missions.")
    try:
        logger.info("return all Missions.")
        return mission.get_all_missions()
    except Exception as e:
        logger.error("Failed to show all Missions")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect the server."
        )

@router.get("/missions/{m_id}")
def mission_by_id(m_id: int):
    logger.info("Start to show mission by ID.")
    try:
        if type(m_id) != int:
            logger.error("Failed to show mission by ID, Invalid ID.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        data = mission.get_mission_by_id(m_id)
        if data is None:
            logger.error("Failed to show mission by ID, ID not exist.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID not exist."
            )
        
        logger.info("return mission by ID.")
        return data
    except Exception:
        logger.error("Failed to show mission by ID.")
        raise


@router.put("/missions/{m_id}/assign/{a_id}")
def assign_mission(m_id: int, a_id:int):
    logger.info("Start to assign mission.")
    try:
        if type(m_id) != int or type(a_id) != int:
            logger.error("Failed to assign mission, Invalid ID.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )

        the_mission = mission.get_mission_by_id(m_id)
        the_agent = agent.get_agent_by_id(a_id)
        open_missions = mission.get_open_missions_by_agent(a_id)

        if the_mission is None:
            logger.error("Failed to assign mission, Mission not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not found")

        if the_agent is None:
            logger.error("Failed to assign mission, Mission not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        if the_mission["status"] != "NEW":
            logger.error("Failed to assign mission, can assign only mission with a status NEW.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="can assign only mission with a status NEW"
            )
        
        if not the_agent["is_active"]:
            logger.error("Failed to assign mission, Agent inactive.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agent inactive."
            )
        
        if len(open_missions) >= 3:
            logger.error("Failed to assign mission, Agent has 3 or more open missions.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Agent {a_id} has 3 or more open missions."
            )
        
        if the_mission["risk_level"] == "CRITICAL":
            if the_agent["agent_rank"] == "Junior":
                logger.error("Failed to assign mission, Agent in Junior level.")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Agent {a_id} in Junior level."
                )
            
            if the_agent["agent_rank"] == "Senior":
                logger.error("Failed to assign mission, Agent in Senior level.")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Agent {a_id} in Senior level."
                )
        change_mission_assign_id = mission.assign_mission(m_id, a_id)
        change_mission_status = mission.update_mission_status(m_id, "ASSIGNED")
        logger.info("Mission assigned.")
        return [change_mission_assign_id,
                change_mission_status]
    except Exception:
        logger.error("Failed to assign mission.")
        raise




@router.put("/missions/{m_id}/start")
def start_mission(m_id: int):
    logger.info("Starting mission.")
    try:
        the_mission = mission.get_mission_by_id(m_id)

        if the_mission is None:
            logger.error("Failed to start mission, Mission not fount.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not fount")
        
        if the_mission["status"] != "ASSIGNED":
            logger.error("Failed to start mission, cannot start mission with a status not ASSIGNED.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cannot start mission with a status not ASSIGNED"
            )
        
        change_mission_status = mission.update_mission_status(m_id, "IN_PROGRESS")
        logger.info("Mission started.")
        return change_mission_status
    except Exception:
        logger.error("Failed to start mission.")
        raise


@router.put("/missions/{m_id}/complete")
def complete_mission(m_id: int):
    logger.info("Start to complete mission.")
    try:
        if type(m_id) != int or type(m_id) != int:
            logger.error("Failed to complete mission, Invalid ID.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )

        the_mission = mission.get_mission_by_id(m_id)
        assign_agent = the_mission["assigned_agent_id"]

        if the_mission is None:
            logger.error("Failed to complete mission, Mission not fount.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not fount")
        
        if the_mission["status"] != "IN_PROGRESS":
            logger.error("Failed to complete mission, cannot complete mission with a status not IN_PROGRESS.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cannot complete mission with a status not IN_PROGRESS"
            )
        
        change_mission_status = mission.update_mission_status(m_id, "COMPLETED")
        increment_agent = agent.increment_completed(assign_agent)
        if increment_agent:
            logger.info("Mission completed.")
            return [change_mission_status,
                    {"message": f"agent {assign_agent} increment complete mission"}]
    
    except Exception:
        logger.error("Failed to complete mission.")
        raise


@router.put("/missions/{m_id}/fail")
def failed_mission(m_id: int):
    logger.info("Start to failed mission.")
    try:
        if type(m_id) != int or type(m_id) != int:
            logger.error("Failed to failed mission, Invalid ID.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )

        the_mission = mission.get_mission_by_id(m_id)
        assign_agent = the_mission["assigned_agent_id"]

        if the_mission is None:
            logger.error("Failed to failed mission, Mission not fount.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not fount")
        
        if the_mission["status"] != "IN_PROGRESS":
            logger.error("Failed to failed mission, cannot failed mission with a status not IN_PROGRESS.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cannot failed mission with a status not IN_PROGRESS"
            )
        
        change_mission_status = mission.update_mission_status(m_id, "FAILED")
        increment_agent = agent.increment_failed(assign_agent)
        if increment_agent:
            logger.info("Mission failed.")
            return [change_mission_status,
                    {"message": f"agent {assign_agent} increment failed mission"}]
    
    except Exception:
        logger.error("Failed to failed mission.")


@router.put("/missions/{m_id}/cancel")
def cancel_mission(m_id: int):
    logger.info("Start to cancel mission.")
    try:
        if type(m_id) != int or type(m_id) != int:
            logger.error("Failed to cancel mission, Invalid ID.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        the_mission = mission.get_mission_by_id(m_id)

        if the_mission is None:
            logger.error("Failed to cancel mission, Mission not fount.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not fount")
        
        if the_mission["status"] != "NEW" and the_mission["status"] != "ASSIGNED":
            logger.error("Failed to cancel mission, cannot cancel mission with a status not NEW or ASSIGNED.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cannot cancel mission with a status not NEW or ASSIGNED"
            )
        
        change_mission_status = mission.update_mission_status(m_id, "CANCELLED")
        if change_mission_status:
            logger.info("Mission cancelled.")
            return {"message": f"mission {m_id} cancelled."}
    
    except Exception:
        logger.error("Failed to cancel mission.")
        raise 