# Funções para inserção e consulta de dados no banco
import pandas as pd
from sqlalchemy.sql import text


def insert_weather_data(conn, weather_data):
    """ INSERE dados de clima no banco de dados PostgreSQL.
    Parametros: 
        conn: Conexão com o banco de dados (ou engine do SQLAlchemy)
        weather_data: Lista de tuplas com dados para inserir"""

    query = text("""
    INSERT INTO clima (cidade, temperatura, umidade, descricao, data_consulta)
    VALUES (:cidade, :temperatura, :umidade, :descricao, :data_consulta)
    """)
    try:
        with conn.connect() as connection:
            with connection.begin(): # Inicia uma transação
                for data in weather_data:
                    connection.execute(query, {
                        "cidade": data[0],
                        "temperatura": data[1],
                        "umidade": data[2],
                        "descricao": data[3],
                        "data_consulta": data[4],
                    })
            print("Dados inseridos com sucesso")
    except Exception as e:
        print(f"Erro ao inserir dados no banco: {e}")
        

def fetch_weather_data_from_db(engine, query):
    #Realiza consultas no banco e retorna como DataFrame.

    try: 
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return pd.DataFrame()