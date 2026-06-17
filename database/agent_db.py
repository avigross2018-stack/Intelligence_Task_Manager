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
        return {"message": "Failed to create new agent"}


    def get_agent_by_id(self, agent_id: int) -> dict | None:
        con = self.db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM agents WHERE id = %s
        """, (agent_id,))
        data = cur.fetchone()
        cur.close()
        con.close()
        return data


    def update_agent(self, agent_id: int, data: dict) -> dict:
        keys = [f"{k} = %s" for k in data]
        values = list(data.values())
        values.append(agent_id)
        clean_keys = ", ".join(keys)

        sql = f"UPDATE agents SET {clean_keys} WHERE id = %s"
        con = self.db.get_connection()
        cur = con.cursor()
        cur.execute(sql, tuple(values))
        con.commit()
        change = cur.rowcount > 0
        cur.close()
        con.close()
        if change:
            return {"message": f"agent {agent_id} updated."}
        return {"message": f"agent {agent_id} is not updated."}


    def deactivate_agent(self, agent_id: int) -> dict:
        con = self.db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            UPDATE agents SET (is_active = FALSE WHERE id = %s)
        """, (agent_id,))
        con.commit()
        change = cur.rowcount > 0
        cur.close()
        con.close()
        if change:
            return {"message": f"agent {agent_id} is not active."}
        return {"message": f"Failed to deactivate agent {agent_id}."}


    def increment_completed(self, agent_id: int) -> dict:
        pass


    def get_agent_performance(self, agent_id: int) -> dict:
        pass


    def count_active_agents(self) -> dict:
        pass