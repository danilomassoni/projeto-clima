# Funções para inserção e consulta de dados no banco
import pandas as pd

def insert_weather_data(conn, data):

    try:
        with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO clima (cidade, temperatura, umidade, descricao, data_consulta)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, data)
            conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def fetch_weather_data(conn, query):
    #Realiza consultas no banco e retorna como DataFrame.

    try: 
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return pd.DataFrame()