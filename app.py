# Arquivo principal para execução do projeto
import pandas as pd
from api.api_client import fetch_weather_from_api
from database.db_connection import connect_to_postgresql
from database.data_operations import fetch_weather_data_from_db, insert_weather_data
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
    dados_clima = fetch_weather_from_api(cidade)

    if dados_clima:
        # 2 Inserir dados no banco de dados
        weather_data = [(dados_clima['cidade'], dados_clima['temperatura'],
                                        dados_clima['umidade'], dados_clima['descricao'], dados_clima['data_consulta'])]
        
        print(f"Inserindo dados de {cidade} no banco de dados....")
        print("Dados para inserção:", weather_data)
              
        try:
            insert_weather_data(conn, weather_data)
                                    
        except Exception as e:
            print(f"Erro ao inserir dados no banco: {e}")
    else:
        print(f"Erro: Os dados retornados não são válidos.")

    # 3 - Consultar os dados do banco de dados
    query = "SELECT cidade, temperatura, umidade, descricao, data_consulta FROM clima WHERE cidade = 'São Paulo'"
    df = fetch_weather_data_from_db(conn, query)

    # 4 Treinar o modelo de regressão
    if not df.empty:
        print("Treinando modelo de regressão")
        modelo, score = train_regression_model(df)
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

cidade = "São Paulo"
print(f"Buscando dados de clima para {cidade}")
dados_clima = fetch_weather_from_api(cidade)
print("Retorno de tech_weather_from_api:", dados_clima)


if __name__ == "__main__":
    main()