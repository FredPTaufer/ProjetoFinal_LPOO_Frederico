import sqlite3
from sqlite3 import Connection


class DatabaseConfig:
    @staticmethod
    def get_connection(db_path: str = "salon.db") -> Connection:
        return sqlite3.connect(db_path)
