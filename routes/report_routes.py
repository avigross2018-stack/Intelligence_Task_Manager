from fastapi import APIRouter, HTTPException, status
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from logger import get_logger


router = APIRouter()

mission = MissionDB()
agent = AgentDB()
logger = get_logger()


@router.get("/reports/summary")
def get_summary():
    logger.info("Start to get summary report.")
    try:
        active_agents = agent.count_active_agents()
        all_missions = mission.count_all_missions()
        open_missions = mission.count_open_missions()
        complete_missions = mission.count_by_status("COMPLETED")
        failed_missions = mission.count_by_status("FAILED")
        cancel_missions = mission.count_by_status("CANCELLED")
        logger.info("Return summary report.")
        return {
            "active_agents_count": active_agents,
            "total_missions": all_missions,
            "open_missions": open_missions,
            "completed_missions": complete_missions,
            "failed_missions": failed_missions,
            "cancel_missions": cancel_missions
                }
    except Exception:
        logger.error("Failed to return summary report.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect the server."
        )



@router.get("/reports/missions-by-status")
def missions_by_status_report():
    logger.info("Start to get mission by status report.")
    try:
        open_missions = mission.count_open_missions()
        in_progress_missions = mission.count_by_status("IN_PROGRESS")
        complete_missions = mission.count_by_status("COMPLETED")
        failed_missions = mission.count_by_status("FAILED")
        cancel_missions = mission.count_by_status("CANCELLED")
        logger.info("Return mission by status report.")
        return {
            "open": open_missions,
            "in_progress": in_progress_missions,
            "completed": complete_missions,
            "failed": failed_missions,
            "canceled": cancel_missions
            }
    
    except Exception:
        logger.info("Failed to get mission by status report.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect the server."
        )



@router.get("/reports/top-agent")
def top_agent():
    logger.info("Start to get top agent.")
    try:
        top_agent =  mission.get_top_agent()
        if not top_agent:
            logger.error("Failed to get top agent, No top agent.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No top agent"
            )
        
        logger.info("Return top agent.")
        return top_agent
    except Exception:
        logger.error("Failed to get top agent.")
        raise 