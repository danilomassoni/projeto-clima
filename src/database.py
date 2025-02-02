# Módulo para conectar ao PostgreSQL e salvar as previsões

import psycopg2
from psycopg2 import sql
import pandas as pd
from datetime import datetime  # <-- Importação necessária para salvar a data/hora

class Database: 
    def __init__(self, dbname="previsao_climatica", user="postgres", password="1234", host="localhost", port="5432"):
        self.dbname = dbname
        self.user=user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        """Estabelecer conexão com o banco PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password = self.password,
                host=self.host,
                port=self.port
            )
            print("Conectado ao banco de dados com sucesso!")
        except Exception as e:
            print(f"Erro ao se conectar ao banco de dados: {e}")

    def create_table(self):
        """Cria a tabela para armazenar as previsões, caso ela não exista"""
        if self.conn is None:
            self.connect()
        
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                        CREATE TABLE IF NOT EXISTS previsoes (
                            id SERIAL PRIMARY KEY, 
                            data DATE NOT NULL,
                            yhat FLOAT NOT NULL,
                            yhat_lower FLOAT NOT NULL,
                            yhat_upper FLOAT NOT NULL,
                            data_previsao TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- <-- Adicionando a nova coluna
                        );
                """)
                self.conn.commit()
                print("Tabela 'previsoes' verificada/criada com sucesso!")

        except Exception as e:
            print(f"Erro ao criar a tabela: {e}")

    def save_forecast(self, forecast_df):
        """Salva previsões no banco de dados"""
        if self.conn is None:
            self.connect()

        try:
            with self.conn.cursor() as cur:
                for _, row in forecast_df.iterrows():
                    print(f"Inserindo: {row['ds']}, {row['yhat']}, {row['yhat_lower']}, {row['yhat_upper']}, {datetime.now()}")  # <-- Print atualizado

                    cur.execute("""
                        INSERT INTO previsoes (data, yhat, yhat_lower, yhat_upper, data_previsao)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (row['ds'], row['yhat'], row['yhat_lower'], row['yhat_upper'], datetime.now()))
                
                self.conn.commit()
                print("✅ Previsões salvas no banco com timestamp!")

        except Exception as e:
            print(f"❌ Erro ao salvar previsões: {e}")

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            print("Conexão com o banco fechada.")
