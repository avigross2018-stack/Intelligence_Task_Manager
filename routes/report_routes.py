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
    try:
        active_agents = agent.count_active_agents()
        all_missions = mission.count_all_missions()
        open_missions = mission.count_open_missions()
        complete_missions = mission.count_by_status("COMPLETED")
        failed_missions = mission.count_by_status("FAILED")
        cancel_missions = mission.count_by_status("CANCELLED")
        return {
            "active_agents_count": active_agents,
            "total_missions": all_missions,
            "open_missions": open_missions,
            "completed_missions": complete_missions,
            "failed_missions": failed_missions,
            "cancel_missions": cancel_missions
                }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect the server."
        )



@router.get("/reports/missions-by-status")
def missions_by_status_report():
    try:
        open_missions = mission.count_open_missions()
        in_progress_missions = mission.count_by_status("IN_PROGRESS")
        complete_missions = mission.count_by_status("COMPLETED")
        failed_missions = mission.count_by_status("FAILED")
        cancel_missions = mission.count_by_status("CANCELLED")
        return {
            "open": open_missions,
            "in_progress": in_progress_missions,
            "completed": complete_missions,
            "failed": failed_missions,
            "canceled": cancel_missions
            }
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect the server."
        )



@router.get("/reports/top-agent")
def top_agent():
    try:
        agent =  mission.get_top_agent()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No top agent"
            )
    except Exception:
        raise 