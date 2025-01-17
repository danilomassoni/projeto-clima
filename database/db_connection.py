# Funções para conexão com o PostgreSQL

import psycopg2 

def connect_to_postgresql():

    try: 
        conn = psycopg2.connect(
            dbname="clima_dados",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None