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
        con = self.db.get_connection()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO agents (name, specialty, is_active, completed_missions,
                    failed_missions, agent_rank) VALUES (
                    %s, %s, %s, %s, %s, %s)
        """, tuple(data.name, data.specialty, data.is_active, data.completed_missions,
                   data.failed_missions, data.agent_rank))
        con.commit()
        change = cur.rowcount > 0
        agent_id = cur.lastrowid
        cur.close()
        con.close()
        if change > 0:
            return {"message": "new agent created",
                    "detail": {"id": agent_id, "name": data.name, "specialty": data.specialty,
                               "is_active": data.is_active, "completed_missions": data.completed_missions,
                               "failed_missions": data.completed_missions, "agent_rank": data.agent_rank}}


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