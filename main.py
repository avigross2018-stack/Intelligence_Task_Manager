from database.agent_db import AgentDB
from utils.models import CreateAgent

a = CreateAgent(name="bbb", specialty="run", agent_rank="Junior")
print(a.__str__())
agent = AgentDB()
print(agent.update_agent(1, {"name": "ccc"}))