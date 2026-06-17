from database.mission_db import MissionDB
from utils.models import CreateAgent, CreateMission
from database.agent_db import AgentDB
m = CreateMission(title="bbb", description="ccc", location="US", difficulty=7, importance=5, assigned_agent_id=2)
mission = MissionDB()
a = AgentDB()
print(a.increment_completed(2))