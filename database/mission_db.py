from database.db_connection import DBConnector
from utils.models import CreateAgent
from utils.exceptions import DataNotExist


class AgentDB:

    db = DBConnector()

    def get_all_agents(self) -> list:
        con = self.db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM agents
        """)
        data = cur.fetchall()
        cur.close()
        con.close()
        return data


    def create_agent(self, data: CreateAgent) -> dict:
        pass


    def get_agent_by_id(self, agent_id: int) -> dict | None:
        con = self.db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM agents WHERE id = %s
        """, (agent_id,))
        data = cur.fetchone()
        if data is None:
            raise DataNotExist("ID not found.")
        cur.close()
        con.close()
        return data


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