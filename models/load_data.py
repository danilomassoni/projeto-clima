# Código para inserir os dados no PostgreSQL

import psycopg2 
import pandas as pd 

def load_csv_to_postgres(csv_filepath, db_config):
    """
    Carrega os dados de uma arquivo CSV para uma tablea no PostgreSQL.

    Args:
        csv_filepath (str): Caminho para o arquivo CSV.
        db_config (dict): Configurações de conexão com o banco de dados.
    
    """
    conn = None # Inicializa a conexão como None para evitar erros no finally

    try:
        # Leitura do CSV
        df = pd.read_csv(csv_filepath, sep=';')

        # Conectar com o banco de dados PostgreSQL
        conn = psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        cursor = conn.cursor()
        print("Conexão estabelecida com o banco de dados.")

        # Iterar pelas linhas do DataFrame e inserir no banco
        for index, row in df.iterrows():
            cursor.execute(
                """
                INSERT INTO temperaturas_sp (ano, mes, temperatura)
                VALUES (%s, %s, %s)
                """,
                (row['ano'], row['mes'], row['temperatura'])
            )

        # Salvar alterações
        conn.commit()
        print("Dados inseridos na tabela 'temperaturas_sp' com sucesso!")
    
    except Exception as e:
        print(f"Erro ao carregar dados no banco: {e}")

    finally:
        # Fechar a conexão com o banco
        if conn:
            cursor.close()
            conn.close()
            print("Conexão com o banco de dados PostgreSQL encerrada.")

if __name__ == "__main__":
    # Configurações do banco de dados
    db_config = {
    'dbname': 'clima_dados',  # Nome do banco de dados
    'user': 'postgres',       # Nome do usuário PostgreSQL
    'password': '1234',       # Senha do usuário
    'host': 'localhost',      # Host onde o banco está rodando
    'port': 5432              # Porta padrão do PostgreSQL
    }

    # Caminho para o arquivo em CSV
    csv_filepath = r"C:\Users\masso\OneDrive\Área de Trabalho\danilo\estudos-python\projeto-clima\data\processed\dataframe_formatado.csv"

    # Executar todo o carregamento para o banco PostgreSQL
    load_csv_to_postgres(csv_filepath, db_config)