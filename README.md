# Projeto Clima

Este projeto tem como objetivo buscar dados de clima, armazenar esses dados em um banco de dados PostgreSQL, treinar um modelo de regressão e gerar visualizações dos dados reais vs. previstos.

## Estrutura do Projeto

- `app.py`: Arquivo principal para execução do projeto.
- `api/api_client.py`: Contém a função para buscar dados de clima da API.
- `database/db_connection.py`: Contém a função para conectar ao banco de dados PostgreSQL.
- `database/data_operations.py`: Contém funções para inserir e buscar dados do banco de dados.
- `models/regression_model.py`: Contém a função para treinar o modelo de regressão.
- `visualizations/plot_utils.py`: Contém a função para gerar visualizações dos dados.

## Instalação

1. Clone o repositório:
   ```sh
   git clone git@github.com:danilomassoni/projeto-clima.git
   cd projeto-clima