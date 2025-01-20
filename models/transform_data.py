# Código para transformar os dados
import pandas as pd
import os



def transform_data(filepath):
    """ 
    Transforma os dados em XLS para o formato desejado para ser inserido no PostgreSQL
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo não foi encontrado: {filepath}")

    try:
        # Carregar dados do Excel
        df = pd.read_excel(filepath)
    except ImportError as e:
        raise ImportError("Erro ao ler o arquivo Excel. Certifique-se de que as bibliotecas 'openpyxl' ou 'xlrd' estão instaladas.") from e

    # Criar uma cópia do DataFrame original para preservar os dados
    df_original = df.copy()

    # Selecionar as colunas de meses, excluindo 'ANUAL'
    colunas_meses = [col for col in df.columns if col not in ['Anos/Meses', 'ANUAL']]

    # Criar um novo DataFrame formatado
    df_formatado = pd.melt(df_original, id_vars=['Anos/Meses'], value_vars=colunas_meses,
                           var_name='mes', value_name='temperatura')

    # Renomear e ajustar o formato
    df_formatado.rename(columns={'Anos/Meses': 'ano'}, inplace=True)
    
    # Verificar e corrigir os valores de temperatura
    df_formatado['temperatura'] = df_formatado['temperatura'].apply(
        lambda x: str(x).replace(',', '.') if isinstance(x, str) else x
    )

    # Converter temperaturas para tipo float
    df_formatado['temperatura'] = pd.to_numeric(df_formatado['temperatura'], errors='coerce')

    return df_formatado


# Testar a função
if __name__ == "__main__":
    # Definir o caminho do arquivo
    filepath = r"C:\Users\masso\OneDrive\Área de Trabalho\danilo\estudos-python\projeto-clima\data\raw\2023_temperatura_1933_2023_1723127628.xlsx"

    processed_dir = r"C:\Users\masso\OneDrive\Área de Trabalho\danilo\estudos-python\projeto-clima\data\processed"
    output_filepath = os.path.join(processed_dir, "dataframe_formatado.csv")
    try:
        df_formatado = transform_data(filepath)
        print("Novo DataFrame formatado:")
        print(df_formatado.head())

        df_formatado.to_csv(output_filepath, index=False, sep=";")
    
    except Exception as e:
        print(f"Erro ao processo o arquivo {e}")
