# Arquivo principal para execução do projeto
import pandas as pd
from api.api_client import fetch_weather_from_api
from database.db_connection import connect_to_postgresql
from database.data_operations import fetch_weather_data, insert_weather_data
from models.regression_model import train_regression_model
from visualizations.plot_utils import plot_real_vs_predicted

def main():
    # Conectar com o banco de dados PostgreSQL
    conn = connect_to_postgresql()
    if not conn:
        print("Falha na conexão com o banco de dados.")
        return

    # 1 - Obter dados da API para a cidade de São Paulo
    cidade = "São Paulo"
    print(f"Buscando dados de clima para a cidade de {cidade}.....")
    dados_clima = fetch_weather_data

    if dados_clima:
        # 2 Inserir dados no banco de dados
        print(f"Inserindo dados de {cidade} no banco de dados....")
        insert_weather_data(conn, [(dados_clima['cidade'], dados_clima['temperatura'],
                                    dados_clima['umidade'], dados_clima['descricao'], dados_clima['data_consulta'])])
    else:
        print(f"Não foi possível obter dados de {cidade}.")

    # 3 - Consultar os dados do banco de dados
    query = "SELECT cidade, temperatura, umidade, descricao, data_consulta FROM clima WHERE cidade = 'Sao Paulo'"
    df = fetch_weather_data(conn, query)

    # 4 Treinar o modelo de regressão
    if not df.empty:
        print("Treinando modelo de regressão")
        modelo, score = train_regression_model
        print(f"Modelo treinado com sucesso! Acurácia do modelo: {score:.2f}")

        # 5 - Visualizar os resultados
        print("Gerando gráficos de comparação......")
        y_real = df['temperatura']
        y_pred = modelo.predict(df[['umidade', 'dia_do_ano']])
        plot_real_vs_predicted(y_real, y_pred)

    else:
        print("Nenhum dado disponível para treino no banco de dados.")

    # Fechar conexão com o Banco de Dados
    conn.close()

if __name__ == "__main__":
    main()