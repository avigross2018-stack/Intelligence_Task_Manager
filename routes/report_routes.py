from fastapi import APIRouter, HTTPException, status




router = APIRouter()




@router.get("/reports/summary")
def get_summary():
    pass



@router.get("/reports/missions-by-status")
def missions_by_status_report():
    pass



@router.get("/reports/top-agent")
def top_agent():
    pass