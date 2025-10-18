"""Módulo para gerenciar conexões com SQLALCHEMY com PostgreSQL."""

import sqlite3
import time
from pathlib import Path
from typing import Optional

from dotenv import dotenv_values
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase


class ConnectionDatabase:
    """Gerencia conexão SqlAlchemy com PostgreSQL."""

    def __init__(
        self,
        environment: str,
        db_name: str,
        base: Optional[type[DeclarativeBase]] = None,
        sgbd_name: str = "postgresql",
        connection_folder: str = "databases_connection",
    ) -> None:
        """Inicializa uma instância de ConnectionDatabase.

        Inicializa os atributos necessários para gerenciar conexões com o banco
        de dados usando SQLAlchemy (ou sqlite quando aplicável).

        Args:
            environment (str): Nome do ambiente (ex.: "dev", "prod", "test").
            db_name (str): Nome do banco de dados ou arquivo de banco (para sqlite).
            base (Optional[object], optional): Base declarativa do SQLAlchemy usada
                para criação de tabelas/mapeamentos. Defaults to None.
            sgbd_name (str, optional): Identificador do SGBD a ser usado na
                connection string (ex.: "postgresql", "sqlite").
                Defaults to "postgresql".
            connection_folder (str, optional): Pasta onde ficam os arquivos de
                configuração/connection string. Defaults to "databases_connection".

        Attributes:
            sgbd_name (str): Nome do SGBD.
            environment (str): Ambiente atual.
            db_name (str): Nome do banco de dados.
            connection_folder (str): Pasta de conexões.
            current_dir (Optional[Path]): Diretório atual (inicialmente None).
            path_file (Optional[Path]): Path do arquivo de conexão (inicialmente None).
            path (Optional[Path]): Path calculado (inicialmente None).
            sqlite_conn (Optional[sqlite3.Connection]):
                Conexão sqlite quando usada (inicialmente None).
            base (Optional[object]): Base declarativa do SQLAlchemy fornecida.
            engine: Instância do engine SQLAlchemy (inicialmente None).
        """
        self.sgbd_name = sgbd_name
        self.environment = environment
        self.db_name = db_name
        self.connection_folder = connection_folder
        self.current_dir: Optional[Path] = None
        self.path_file: Optional[Path] = None
        self.path: Optional[Path] = None
        self.sqlite_conn: Optional[sqlite3.Connection] = None
        self.base = base
        self.engine: Optional[Engine] = None

    def initialize_engine(self) -> Optional[Engine]:
        """Cria a URL de conexão com SqlAlchemy."""
        self.current_dir = Path(__file__).resolve().parent
        self.path = self.current_dir.parent.joinpath(
            self.connection_folder, self.sgbd_name
        )

        if self.sgbd_name == "postgresql":
            self.path_file = self.path.joinpath(
                f".env.{self.environment}_{self.db_name}"
            )

            if not self.path_file.is_file():
                raise FileNotFoundError(
                    f"Configuration file '{self.path_file}' not found."
                )

            env_vars = dotenv_values(dotenv_path=self.path_file)

            settings = {
                "db_host": env_vars["DB_HOST"],
                "db_user": env_vars["DB_USER"],
                "db_pass": env_vars["DB_PASSWORD"],
                "db_name": env_vars["DB_NAME"],
                "db_port": env_vars["DB_PORT"],
            }

            connection_string = f"postgresql+psycopg2://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"
            engine = create_engine(connection_string)
            return engine
        else:
            raise ValueError(f"SGBD '{self.sgbd_name}' não suportado.")

    def connect(
        self, max_retries: int = 5, wait_seconds: int = 1
    ) -> Optional[Engine] | None:
        """Estabelece conexão com o banco de dados com tentativas de reconexão.

        Tenta estabelecer uma conexão com o banco de dados usando o engine inicializado.
        Em caso de falha, faz novas tentativas após intervalos de espera.

        Args:
            max_retries (int, optional): Número máximo de tentativas de conexão.
            Defaults to 5.
            wait_seconds (int, optional): Tempo de espera em segundos entre tentativas.
            Defaults to 1.

        Returns:
            Engine: Objeto engine do SQLAlchemy se a conexão for bem sucedida.
            None: Se todas as tentativas de conexão falharem.

        Raises:
            OperationalError: Erro de conexão com o banco de dados após todas as.
            tentativas.
        """
        for number in range(1, max_retries + 1):
            try:
                self.engine = self.initialize_engine()

                if self.engine:
                    with self.engine.connect() as conn:
                        conn.execute(text("SELECT 1"))
                    return self.engine
            except OperationalError:
                print("Failed to connect!")
                if number == max_retries:
                    print("Maximum number of save attempts reached.")
                    return None
                else:
                    time.sleep(wait_seconds)
        return None

    def create_schema(self, max_retries: int = 5, wait_seconds: int = 1) -> None:
        """Cria o esquema do banco de dados usando a base declarativa fornecida.

        Tenta criar todas as tabelas definidas na base declarativa do SQLAlchemy.
        Em caso de falha, faz novas tentativas após intervalos de espera.

        Args:
            max_retries (int, optional): Número máximo de tentativas de criação.
            Defaults to 5.
            wait_seconds (int, optional): Tempo de espera em segundos entre tentativas.
            Defaults to 1.

        Raises:
            OperationalError: Erro ao criar as tabelas após todas as tentativas.
        """
        for number in range(1, max_retries + 1):
            try:
                if self.base is not None and self.engine is not None:
                    self.base.metadata.create_all(bind=self.engine)
                    return
            except OperationalError as e:
                print(f"Failed to create table:{e}")
                if number == max_retries:
                    raise
                else:
                    time.sleep(wait_seconds)
