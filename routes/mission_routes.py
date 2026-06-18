from fastapi import APIRouter, HTTPException, status
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from utils.models import CreateMission


router = APIRouter()

mission = MissionDB()
agent = AgentDB()

@router.post("/missions",
             status_code=status.HTTP_201_CREATED)
def new_mission(data: CreateMission):
    try:
        if data.status not in ('NEW', 'ASSIGNED', 'IN_PROGRESS', 
                               'COMPLETE', 'FAILED', 'CANCELLED'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status"
            )

        if data.difficulty > 10 or data.difficulty < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid difficulty (1-10)"
            )
        
        if data.importance > 10 or data.importance < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid importance (1-10)"
            )
        
        return mission.create_mission(data)
    
    except Exception:
        raise


@router.get("/missions")
def all_missions():
    try:
        return mission.get_all_missions()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to connect the server."
        )

@router.get("/missions/{m_id}")
def mission_by_id(m_id: int):
    try:
        if type(m_id) != int:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        data = mission.get_mission_by_id(m_id)
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID not exist."
            )
    except Exception:
        raise


@router.put("/missions/{m_id}/assign/{a_id}")
def assign_mission(m_id: int, a_id:int):
    try:
        if type(m_id) != int or type(a_id) != int:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )

        the_mission = mission.get_mission_by_id(m_id)
        the_agent = agent.get_agent_by_id(a_id)
        open_missions = mission.get_open_missions_by_agent(a_id)

        if the_mission is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not fount")

        if the_agent is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not fount"
            )
        
        if the_mission["status"] != "NEW":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="can assign only mission with a status NEW"
            )
        
        if not the_agent["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agent inactive."
            )
        
        if len(open_missions) >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Agent {a_id} has 3 or more open missions."
            )
        
        if the_mission["risk_level"] == "CRITICAL":
            if the_agent["agent_rank"] == "Junior":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Agent {a_id} in Junior level."
                )
            
            if the_agent["agent_rank"] == "Senior":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Agent {a_id} in Senior level."
                )
        change_mission_assign_id = mission.assign_mission(m_id, a_id)
        change_mission_status = mission.update_mission_status(m_id, "ASSIGNED")
        return [change_mission_assign_id,
                change_mission_status]
    except Exception:
        raise




@router.put("/missions/{m_id}/start")
def start_mission(m_id: int):
    try:
        the_mission = mission.get_mission_by_id(m_id)

        if the_mission is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not fount")
        
        if the_mission["status"] != "ASSIGNED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cannot start mission with a status not ASSIGNED"
            )
        
        change_mission_status = mission.update_mission_status(m_id, "IN_PROGRESS")
        return change_mission_status
    except Exception:
        raise


@router.put("/missions/{m_id}/complete")
def complete_mission(m_id: int):
    try:
        if type(m_id) != int or type(m_id) != int:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )

        the_mission = mission.get_mission_by_id(m_id)
        assign_agent = the_mission["assigned_agent_id"]

        if the_mission is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not fount")
        
        if the_mission["status"] != "IN_PROGRESS":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cannot complete mission with a status not IN_PROGRESS"
            )
        
        change_mission_status = mission.update_mission_status(m_id, "COMPLETED")
        increment_agent = agent.increment_completed(assign_agent)
        if increment_agent:
            return [change_mission_status,
                    {"message": f"agent {assign_agent} increment complete mission"}]
    
    except Exception:
        raise


@router.put("/missions/{m_id}/fail")
def failed_mission(m_id: int):
    try:
        if type(m_id) != int or type(m_id) != int:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )

        the_mission = mission.get_mission_by_id(m_id)
        assign_agent = the_mission["assigned_agent_id"]

        if the_mission is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not fount")
        
        if the_mission["status"] != "IN_PROGRESS":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cannot failed mission with a status not IN_PROGRESS"
            )
        
        change_mission_status = mission.update_mission_status(m_id, "FAILED")
        increment_agent = agent.increment_failed(assign_agent)
        if increment_agent:
            return [change_mission_status,
                    {"message": f"agent {assign_agent} increment complete mission"}]
    
    except Exception:
        raise


@router.put("/missions/{m_id}/cancel")
def cancel_mission(m_id: int):
    try:
        if type(m_id) != int or type(m_id) != int:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Invalid ID."
            )
        the_mission = mission.get_mission_by_id(m_id)

        if the_mission is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mission not fount")
        
        if the_mission["status"] != "NEW" and the_mission["status"] != "ASSIGNED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cannot cancel mission with a status not NEW or ASSIGNED"
            )
        
        change_mission_status = mission.update_mission_status(m_id, "CANCELLED")
        if change_mission_status:
            return {"message": f"mission {m_id} cancelled."}
    
    except Exception:
        raise 