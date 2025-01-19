# Código para transformar os dados
import pandas as pd

filepath = "data\2023_precipitacao_pluviometrica_1933_2023_1722878382.xls"

def transform_data(filepath):
    """ 
    Transforma os dados em XLS para o formato desejado para ser inserido no PostgreSQL
    """

    # 1 - Carregar dados do Excel
    df = pd.read_excel(filepath)

    # Selecionar as colunas de meses, tirando o 'ANUAL'
    colunas_meses = [col for col in df.columns if col not in 
                     ['Anos/Meses', 'ANUAL']]
    
    # Transformar meses em linhas
    df_long = pd.melt(df, id_vars=['Anos/Meses'], value_vars=colunas_meses,
                      var_name='mes', value_name='temperatura')
    
    # Renomear e ajustar o formato
    df_long.rename(columns={'Anos/Meses': 'ano'}, inplace=True)
    df_long['temperatura'] = df_long['temperatura'].str.replace(',', '.').astype(float)

    return df_long

