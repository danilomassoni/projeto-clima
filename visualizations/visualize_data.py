# Arquivo para visualização dos dados

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_data_from_db(db_config, query):
    """
    Busca dados do banco PostgreSQL.

    Arg:
        db_config (dict): Configuração do banco de dados.
        query (str): Consulta SQL a ser executada. 

    Returns:
        pd.DataFrame: Dados retornados pelo banco em formato de DataFrame para virar Insights.
          
    
    """

    try:
        # Conectar ao banco
        conn = psycopg2.connect(**db_config)
        print("Conexão estabelecida com o banco de dados.")

        # Executar a consulta e transformar em DataFrame
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"Erro ao buscar dados no banco de dados: {e}")
        return None
    finally:
        if conn:
            conn.close()

def visualize_data(db_config):
    """
    Visualiza os dados climáticos históricos do banco de dados PostgresSQL.

    Args: 
        db_config (dict): Configurações do banco de dados. 

    
    """
    query = "SELECT ano, mes, temperatura FROM temperaturas_sp ORDER BY ano, mes;"

    # Buscar os dados do banco de dados PostgreSQL
    df = fetch_data_from_db(db_config, query)

    if df is not None:
        try:
            # Garantir que os dados estejam no formato correto
            df['ano'] = df['ano'].astype(int)
            df['temperatura'] = df['temperatura'].astype(float)

            # Gráfico de linha
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=df, x='ano', y='temperatura', marker='o')
            plt.title('Variação de Temperatura ao Longo dos anos')
            plt.xlabel('Ano')
            plt.ylabel('Temperatura (ºC)')
            plt.grid(True)
            plt.show()

        except Exception as e:
            print(f"Erro ao processar os dados para visualição: {e}")

    else:
        print("Nenhum dado foi retornado do banco.")

if __name__ == "__main__":
    # Configuração do banco de dados PostgreSQL
    db_config = {
        'dbname': 'clima_dados',
        'user': 'postgres',
        'password': '1234',
        'host': 'localhost',
        'port': 5432
    }

    # Visualização dos dados 
    visualize_data(db_config)