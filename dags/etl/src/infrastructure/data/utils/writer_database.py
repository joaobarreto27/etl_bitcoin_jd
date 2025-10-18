"""Módulo que gerencia a carga em banco de dados, utilizando o Pyspark."""

from pandas import DataFrame
from sqlalchemy import text
from sqlalchemy.engine import Engine


class DatabaseWriter:
    """Gerencia a carga em banco de dados com Spark."""

    def __init__(self, engine: Engine) -> None:
        """Inicializa o escritor de banco de dados.

        Args:
            engine (Engine): Instância do engine SQLAlchemy para conexão com o banco.
        """
        self.engine: Engine = engine
        self.truncate_type: bool = False

    def truncate_data(self, table_name: str) -> None:
        """Executa o comando TRUNCATE na tabela especificada.

        Args:
            table_name (str): Nome da tabela a ser truncada.

        Note:
            A operação só é executada se self.truncate_type for True e
            existir uma conexão válida com o banco (self.engine).
        """
        if self.truncate_type:
            if self.engine:
                with self.engine.connect() as conn:
                    conn.execute(text(f"TRUNCATE TABLE {table_name}"))
                    conn.commit()

    def save_data(self, df: DataFrame, table_name: str) -> None:
        """Salva um DataFrame em uma tabela do banco de dados.

        Args:
            df (DataFrame): DataFrame pandas a ser salvo no banco.
            table_name (str): Nome da tabela onde os dados serão salvos.

        Raises:
            ValueError: Se ocorrer erro ao tentar salvar os dados na tabela.

        Note:
            Se self.truncate_type for True, a tabela será truncada antes da inserção.
            Os dados são sempre inseridos em modo append (if_exists="append").
        """
        if self.truncate_type:
            self.truncate_data(table_name=table_name)
        try:
            df.to_sql(table_name, con=self.engine, if_exists="append", index=False)
            print(f"[SUCCESS] Data saved in table '{table_name}'.")
        except Exception as e:
            raise ValueError(
                f"[ERROR] Failed to save data to table '{table_name}': {e}"
            ) from None
