from database.db_connection import DBConnector
from utils.models import CreateAgent


class AgentDB:

    def get_all_agents(self) -> list:
        pass


    def create_agent(self, data: CreateAgent) -> dict:
        pass


    def get_agent_by_id(self, agent_id: int) -> dict | None:
        pass


    def update_agent(self, agent_id: int, data: dict) -> dict:
        pass


    def deactivate_agent(self, agent_id: int) -> dict:
        pass


    def increment_completed(self, agent_id: int) -> dict:
        pass


    def get_agent_performance(self, agent_id: int) -> dict:
        pass


    def count_active_agents(self) -> dict:
        pass