# Modelo para transformar os dados em Dash

import pandas as pd
from prophet import prophet

def generate_forecast(years_to_predict):
    """
    Gera a previsão climática para os próximos anos

    Args: 
        years_to_predict(int): Número de anos para prever.
    Return:
        pd.DataFrame: DataFrame contendo as previsões
    
    """

    # Carregar os dados históricos
    df = pd.read_csv('../data/processed/data_from_db.csv', sep=';')

    # Preparar os dados para o Prophet
    df['ds'] = pd.to_datetime(df['ano'].astype(str) + '-' + df['mes'].astype(str) + '-01')
    df['y'] = df['temperatura']
    df = df[['ds', 'y']]

    # Criar e ajustar o modelo
    model = Prophet()
    model.fit(df)

    # Gerar previsão
    future = model.make_future_dataframe(periods=years_to_predict * 12, freq='M')
    forecast = model.predict(future)

    # Retornar apenas as colunas importantes 
    return forecast[['ds', 'yhat', 'yahat_lower', 'yahat_upper']]

