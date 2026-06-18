from database.db_connection import DBConnector
from utils.models import CreateMission
from utils.exceptions import DataNotExist


db = DBConnector()
db.create_database()
db.create_tables()

class MissionDB:


    def get_all_missions(self):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM missions
        """)
        data = cur.fetchall()
        cur.close()
        con.close()
        return data


    def get_mission_by_id(self, mission_id: int):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM missions WHERE id = %s
        """, (mission_id,))
        data = cur.fetchone()
        cur.close()
        con.close()
        return data


    def create_mission(self, data: CreateMission):
        risk_level = self.calc_risk_level(data.difficulty, data.importance)
        con = db.get_connection()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO missions (title, description, location, difficulty,
                    importance, status, risk_level, assigned_agent_id) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data.title, data.description, data.location, data. difficulty,
              data.importance, data.status, risk_level, data.assigned_agent_id))
        con.commit()
        change = cur.rowcount > 0
        mission_id = cur.lastrowid
        cur.close()
        con.close()
        if change:
            return self.get_mission_by_id(mission_id)
        return {"message": "Failed to create mission."}


    def assign_mission(self, m_id: int, a_id: int):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            UPDATE missions SET assigned_agent_id = %s WHERE id = %s
        """, (a_id, m_id))
        con.commit()
        change = cur.rowcount > 0
        cur.close()
        con.close()
        if change:
            return {"message": f"mission {m_id} assigned to agent {a_id}"}
        return {"message": f"Failed to assigned mission {m_id}"}


    def update_mission_status(self, m_id: int, status: str):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            UPDATE missions SET status = %s WHERE id = %s
        """, (status, m_id))
        con.commit()
        change = cur.rowcount > 0
        cur.close()
        con.close()
        if change:
            return {"message": f"update status {status} to mission {m_id}"}
        return {"message": f"could not update status {status} to mission {m_id}"}


    def get_open_missions_by_agent(self, a_id: int):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM missions WHERE assigned_agent_id = %s AND (
                    status = 'ASSIGNED' OR status = 'IN_PROGRESS') 
        """, (a_id,))
        data = cur.fetchall()
        cur.close()
        con.close()
        return data


    def count_all_missions(self):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT COUNT(*) AS total_missions FROM missions
        """)
        data = cur.fetchone()
        cur.close()
        con.close()
        return data


    def count_by_status(self, status: str):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT COUNT(*) AS status_count FROM missions WHERE status = %s
        """, (status,))
        data = cur.fetchone()
        cur.close()
        con.close()
        return data


    def count_open_missions(self):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT COUNT(*) AS open_missions FROM missions 
                    WHERE status = 'ASSIGNED' OR status = 'IN_PROGRESS'
        """)
        data = cur.fetchone()
        cur.close()
        con.close()
        return data


    def count_critical_missions(self):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT COUNT(*) AS critical_missions FROM missions WHERE risk_level = 'CRITICAL'
        """)
        data = cur.fetchone()
        cur.close()
        con.close()
        return data


    def get_top_agent(self):
        con = db.get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1
        """)
        data = cur.fetchone()
        cur.close()
        con.close()
        return data


    def calc_risk_level(self, difficulty: int, importance: int):
        calc = difficulty * 2 + importance
        if calc >= 0 and calc <= 9:
            return "LOW"
        elif calc >= 10 and calc <= 17:
            return "MEDIUM"
        elif calc >= 18 and calc <= 24:
            return "HIGH"
        elif calc >= 25:
            return "CRITICAL"




