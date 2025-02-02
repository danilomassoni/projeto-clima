# Projeto Clima

Este projeto tem como objetivo buscar dados de clima, especificamente a temperatura, para a cidade de São Paulo, armazenar esses dados em um banco de dados PostgreSQL, treinar um modelo de regressão e gerar visualizações dos dados reais vs. previstos.

## Estrutura do Projeto

- `app.py`: Arquivo principal para execução do projeto e inicialização do servidor Dash.
- `model.py`: Contém a função para gerar previsões climáticas usando o Prophet.
- `data_loader_model.py`: Realiza o tratamento dos dados. 
- `database.py`: Realiza a conexão com o banco de dados. 
- `data/processed/dataframe_formatado.csv`: Arquivo CSV contendo os dados históricos de clima.

## Instalação

1. Clone o repositório:
   ```sh
   git clone git@github.com:danilomassoni/projeto-clima.git
   cd projeto-clima

2. Crie um ambiente virtual 

3. Instale as dependências:
pip install -r requirements.txt


## Configuração do Banco de dados PostgreSQL

1. Certifique-se de ter o PostgreSQL instalado e em execução.
2. Crie um banco de dados para o projeto.
3. Configure as credenciais de conexão no arquivo app.py ou em um arquivo de configuração separado. No projeto está o padrão PostgreSQL.

## Hora de colocar para rodar o projeto

1. Execute o arquivo app.py:
python app.py

2. Acesse a aplicação em: 
http://127.0.0.1:8050/

## Dependências do projeto

dash
pandas
sqlalchemy
prophet
matplotlib
psycopg2-binary
plotly

