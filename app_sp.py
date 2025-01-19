# Rodar todos os arquivos

import os
from models.transform_data import transform_data
from models.load_data import load_data_to_db
from database.db_connection import get_connection_string

def main():
    # Caminho para o arquivo XLS
    filepath = os.path.join('data', 'data/2023_precipitacao_pluviometrica_1933_2023_1722878382.xls')

    # Transformar os dados
    print("Transformando os dados......")
    df = transform_data(filepath)

    # Configurar o banco de dados
    user = 'postegres'
    password = '1234'
    host = 'localhost'
    port = 5432
    db_name = 'clima_dados'

    connection_string = get_connection_string(user, password, host, port, db_name)

    # Inserir os dados no banco de dados PostgreSQL
    print("Inserindo os dados no banco de dados.....")
    load_data_to_db(df, 'temperaturas', connection_string)
    print("Processo de inserir dados concluído.")

if __name__ == "__main__":
    main()