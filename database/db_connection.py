import mysql.connector
from utils.exceptions import FailedConnectionSql


class DBConnector:

    

    def __init__(self):
        self.host = "localhost"
        self.port = 3320
        self.user = "root"
        self.password = "1234"
        self.database = "Intelligence_db"
    
    def get_connection(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Exception as e:
            raise FailedConnectionSql(str(e))

    def create_database(self):
        con = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
        cur = con.cursor()
        cur.execute("""
            CREATE DATABASE IF NOT EXISTS Intelligence_db
        """)
        con.commit()
        cur.close()
        con.close()

    def create_tables(self):
        con = self.get_connection()
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                    id                  INT AUTO_INCREMENT PRIMARY KEY,
                    name                VARCHAR(50) NOT NULL,
                    specialty           VARCHAR(50) NOT NULL,
                    is_active           BOOLEAN DEFAULT TRUE,
                    completed_missions  INT DEFAULT 0,
                    failed_missions     INT DEFAULT 0,
                    agent_rank          ENUM('Junior', 'Senior', 'Commander')
                    )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                    id                  INT AUTO_INCREMENT PRIMARY KEY,
                    title               VARCHAR(30) NOT NULL,
                    description         TEXT NOT NULL,
                    location            VARCHAR(30) NOT NULL,
                    difficulty          INT NOT NULL,
                    importance          INT NOT NULL,
                    status              ENUM('NEW', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED') DEFAULT 'NEW',
                    risk_level          ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'),
                    assigned_agent_id   INT DEFAULT NULL
                    )
        """)
        con.commit()
        cur.close()
        con.close()