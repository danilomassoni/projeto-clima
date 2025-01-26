import pandas as pd
from prophet import Prophet

def generate_forecast(years_to_predict):
    """
    Gera a previsão climática para os próximos anos.

    Args: 
        years_to_predict (int): Número de anos para prever.

    Returns:
        pd.DataFrame: DataFrame contendo as previsões.
    """
    try:
        # Carregar os dados históricos
        df = pd.read_csv(r'data/processed/dataframe_formatado.csv', sep=';')

        # Criar um mapeamento de meses para corrigir valores
        month_mapping = {
            "JAN.": "01", "FEV.": "02", "MAR.": "03", "ABR.": "04",
            "MAI.": "05", "JUN.": "06", "JUL.": "07", "AGO.": "08",
            "SET.": "09", "OUT.": "10", "NOV.": "11", "DEZ.": "12"
        }

        # Substituir abreviações de meses pelo formato numérico
        df['mes'] = df['mes'].str.upper().map(month_mapping)

        # Preparar os dados para o Prophet
        df['ds'] = pd.to_datetime(df['ano'].astype(str) + '-' + df['mes'] + '-01')
        df['y'] = df['temperatura']
        df = df[['ds', 'y']]

        # Criar e ajustar o modelo
        model = Prophet()
        model.fit(df)

        # Gerar previsão
        future = model.make_future_dataframe(periods=years_to_predict * 12, freq='M')
        forecast = model.predict(future)

        # Retornar apenas as colunas importantes
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
    except Exception as e:
        raise ValueError(f"Erro ao gerar a previsão: {e}")
