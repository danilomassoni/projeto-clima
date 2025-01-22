# Faz previsão da temperatura

import psycopg2
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def fetch_data_from_db(db_config, query):
    """
    Busca dados do banco PostgreSQL

    Args:
        db_config (dict): Configurações do banco.
        query (str): Consulta SQL a ser executada.

    Returns:
        pd.DataFrame: Dados retornado pelo banco em formato de DataFrame.
    
    """
    try: 
        # Conectar com o banco de dados PostgresSQL
        conn = psycopg2.connect(**db_config)
        print("Conexão estabelecida com o banco de dados PostgreSQL.")

        # Executar a consulta e transformar em DataFrame
        df = pd.read_sql(query, conn)
        return df
    
    except Exception as e:
        print(f"Erro ao buscar dados do banco: {e}")
        return None
    
    finally:
        if conn: 
            conn.close()

def forecast_climate(db_config, years_to_predict=5):
    """
    Previsão do clima nos próximsos anos com baso nos dados históricos do banco de dados PostgreSQL.

    Args:
        db_config (dict): Configurações do banco de dados PostgreSQL.
        years_to_predict (init): Numéro de anos que serão previstos.

    
    """

    query = "SELECT ano, mes, temperatura FROM temperaturas_sp ORDER BY ano, mes;"

    # Buscar os dados do banco de dados
    df = fetch_data_from_db(db_config, query)

    if df is not None:
        try:
            # Preparar os dados para o Prophet (Biblioteca de Previsão)
            df['ano'] = pd.to_datetime(df['ano'], format='%Y')
            df['df'] = df['ano']
            df['y'] = df['temperatura']
            df = df[['ds', 'y']]

            # Criar e ajustar o modelo Prophet
            model = Prophet()
            model.fit(df)

            # Criar o DataFrame para previsão
            future = model.make_future_dataframe(periods=years_to_predict * 12, freq='M')
            forecast = model.predit(future)  

            # Plotar a previsão
            model.plot(forecast)
            plt.title('Previsão de Temperatura para os Próximos Anos')
            plt.xlabel('Ano')
            plt.ylabel('Temperatura (ºC)')
            plt.grid(True)
            plt.show()

            # Retornar o DataFrame de previsão
            return forecast
        
        except Exception as e:
            print(f"Erro ao realizar previsão climática: {e}")

    else:
        print("Nenhum dado foi retornado do banco de dados.")

if __name__ == "__main__":
    db_config = {
        'dbname': 'clima_dados',
        'user': 'postgres',
        'password': '1234',
        'host': 'localhost',
        'port': 5432
    }        

    # Prever o clima nos próximos 5 anos
    forecast_df = forecast_climate(db_config, years_to_predict=5)