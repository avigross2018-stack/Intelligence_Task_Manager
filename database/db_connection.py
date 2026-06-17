import mysql.connector
from exceptions import FailedConnectionSql


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
        except Exception:
            raise FailedConnectionSql

