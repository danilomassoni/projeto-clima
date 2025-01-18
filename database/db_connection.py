# Funções para conexão com o PostgreSQL
from sqlalchemy import create_engine

def connect_to_postgresql():

    try: 
        engine = create_engine(
            "postgresql+psycopg2://postgres:1234@localhost:5432/clima_dados"
        )
        """ conn = psycopg2.connect(
            dbname="clima_dados",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432" """
        print("Conexão com PostgreSQL estabelecida")
        return engine
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None