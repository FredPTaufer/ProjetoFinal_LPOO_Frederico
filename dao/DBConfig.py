import psycopg2
from psycopg2 import Error


class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            conexao = psycopg2.connect(
                user     = "postgres",
                password = "postgres",
                host     = "localhost",
                port     = "5432",
                database = "lpoo_projeto_Frederico"
            )
            return conexao
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None