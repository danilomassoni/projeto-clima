# Código para inseriro os dados no PostgreSQL

from sqlalchemy import create_engine


def load_data_to_db(df, table_name, connection_string):

    """
    Insere os dados transformados no banco de dados PostgreSQL

    Argumentos: df(pd.DataFrame): Dados transformados.
                table_name (str): Nome da tabela no banco de dados.
                connection_string(str): String de conexão com o PostgreSQL.
    """

    # Criar a conexão com o banco PostgreSQL
    engine = create_engine(connection_string)

    # Inserir os dados no banco de dados
    with engine.connect() as conn:
        df.to_sql(table_name, conn, if_exists='append', index=False)
    print(f'Dados inseridos na tablea {table_name}.')

    