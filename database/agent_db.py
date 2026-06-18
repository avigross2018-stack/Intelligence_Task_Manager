from database.db_connection import DBConnector
from utils.models import CreateAgent
from utils.exceptions import DataNotExist


db = DBConnector()
db.create_database()
db.create_tables()

class AgentDB:

    
    def get_all_agents(self) -> list:
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM agents
        """)
        data = cur.fetchall()
        cur.close()
        con.close()
        return data


    def create_agent(self, data: CreateAgent) -> dict:
        con = db.get_connection()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)
        """, (data.name, data.specialty, data.agent_rank))
        con.commit()
        change = cur.rowcount > 0
        agent_id = cur.lastrowid
        cur.close()
        con.close()
        if change:
            return self.get_agent_by_id(agent_id)
        return {"message": "Failed to create new agent"}


    def get_agent_by_id(self, agent_id: int) -> dict | None:
        con = db.get_connection()
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
        con = db.get_connection()
        cur = con.cursor()
        cur.execute(sql, tuple(values))
        con.commit()
        change = cur.rowcount > 0
        cur.close()
        con.close()
        return change


    def deactivate_agent(self, agent_id: int) -> dict:
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            UPDATE agents SET is_active = FALSE WHERE id = %s
        """, (agent_id,))
        con.commit()
        change = cur.rowcount > 0
        cur.close()
        con.close()
        if change:
            return {"message": f"agent {agent_id} deactivate."}
        return {"message": f"Failed to deactivate agent {agent_id}."}


    def increment_completed(self, agent_id: int) -> dict:
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            UPDATE agents SET completed_missions = completed_missions + 1
                    WHERE id = %s
        """, (agent_id,))
        con.commit()
        change = cur.rowcount > 0
        cur.close()
        con.close()
        return change


    def increment_failed(self, agent_id: int) -> dict:
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            UPDATE agents SET failed_missions = failed_missions + 1
                    WHERE id = %s
        """, (agent_id,))
        con.commit()
        change = cur.rowcount > 0
        cur.close()
        con.close()
        return change


    def get_agent_performance(self, agent_id: int) -> dict:
        con = db.get_connection()
        cur = con.cursor(dictionary=True)

        cur.execute("""
            SELECT completed_missions FROM agents WHERE id = %s 
        """, (agent_id,))
        completed = cur.fetchone()["completed_missions"]

        cur.execute("""
            SELECT failed_missions FROM agents WHERE id = %s 
        """, (agent_id,))
        failed = cur.fetchone()["failed_missions"]
        
        total = completed + failed

        try:
            success_rate = 100 / total * completed
        except ZeroDivisionError:
            success_rate = 0

        cur.close()
        con.close()
        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "success_rate": f"{success_rate} %"
        }


    def count_active_agents(self) -> dict:
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT COUNT(*) AS amount_of_active_agents FROM agents WHERE is_active = TRUE
        """)
        data = cur.fetchone()["amount_of_active_agents"]
        cur.close()
        con.close()
        return data