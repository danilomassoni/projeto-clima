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
    
def get_connection_string(user, password, host, port, db_name):
    """
    Retorna a string de conexão para o banco PostgreSQL

    Args:
        user (str): Usuário do banco.
        password (str): Senha do banco.
        host (str): host do banco.
        port (int): Porta do banco.
        db_name (str): Nome do banco.
    
    Returns: 
        str: String de conexão
             
    """
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'