# Faz previsão da temperatura

from sqlalchemy import create_engine
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def fetch_data_from_db(db_config, query):
    """
    Busca dados do banco PostgreSQL.

    Args:
        db_config (dict): Configurações do banco.
        query (str): Consulta SQL a ser executada.

    Returns:s
        pd.DataFrame: Dados retornados pelo banco em formato DataFrame.
    """
    try:
        # Criar a string de conexão do SQLAlchemy
        engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}")
        
        # Executar a consulta e transformar em DataFrame
        df = pd.read_sql(query, con=engine)
        print("Dados buscados do banco com sucesso.")
        return df
    except Exception as e:
        print(f"Erro ao buscar dados do banco: {e}")
        return None

def forecast_climate(db_config, years_to_predict=20):
    """
    Previsão do clima nos próximos anos com base nos dados históricos do banco.

    Args:
        db_config (dict): Configurações do banco de dados PostgreSQL.
        years_to_predict (int): Número de anos que serão previstos.
    """
    query = "SELECT ano, mes, temperatura FROM temperaturas_sp ORDER BY ano, mes;"

    # Buscar os dados do banco
    df = fetch_data_from_db(db_config, query)

    if df is not None:
        try:
            # Mapeamento de meses para números
            month_mapping = {
                "JAN.": "01", "FEV.": "02", "MAR.": "03", "ABR.": "04",
                "MAI.": "05", "JUN.": "06", "JUL.": "07", "AGO.": "08",
                "SET.": "09", "OUT.": "10", "NOV.": "11", "DEZ.": "12"
            }

            # Substituir abreviações por valores númericos
            df['mes'] = df['mes'].str.upper().map(month_mapping)

            # Remover linhas com meses inválidos (não mapeados)
            df = df.dropna(subset=['mes'])


            # Criar a coluna 'ds' no formato datetime
            df['ds'] = pd.to_datetime(df['ano'].astype(str) + '-' + df['mes'] + '-01', format='%Y-%m-%d')
            df['y'] = df['temperatura']

            # Filtrar as colunas necessárias para o Prophet
            df_prophet = df[['ds', 'y']].copy()

            # Criar e ajustar o modelo Prophet
            model = Prophet()
            model.fit(df_prophet)

            # Criar o DataFrame para previsão
            future = model.make_future_dataframe(periods=years_to_predict * 12, freq='M')
            forecast = model.predict(future)

            # Plotar a previsão
            model.plot(forecast)
            plt.title('Previsão de Temperatura para os Próximos Anos')
            plt.xlabel('Ano')
            plt.ylabel('Temperatura (°C)')
            plt.grid(True)
            plt.show()

            # Retornar o DataFrame de previsão
            return forecast

        except Exception as e:
            print(f"Erro ao realizar previsão climática: {e}")
    else:
        print("Nenhum dado foi retornado do banco.")

if __name__ == "__main__":
    # Configurações do banco de dados
    db_config = {
        'dbname': 'clima_dados',
        'user': 'postgres',
        'password': '1234',
        'host': 'localhost',
        'port': 5432
    }

    # Prever o clima nos próximos 20 anos
    forecast_df = forecast_climate(db_config, years_to_predict=20)

    # Salvar o resultado da previsão
    if forecast_df is not None:
        output_path = r"C:\Users\masso\OneDrive\Área de Trabalho\danilo\estudos-python\projeto-clima\data\processed\forecast.csv"
        forecast_df.to_csv(output_path, index=False, sep=';')
        print(f"Previsão salva em {output_path}")
