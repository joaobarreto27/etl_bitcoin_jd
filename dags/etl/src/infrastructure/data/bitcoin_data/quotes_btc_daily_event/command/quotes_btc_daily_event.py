"""Gerencia o comando de executar a consulta a API e salva no banco de dados."""

from infrastructure.data.bitcoin_quotes.quotes_btc_daily_event.service import (
    QuotesBtcDailyEventService,
)
from infrastructure.data.utils import (
    ConnectionDatabase,
    DatabaseWriter,
)
from pandas import DataFrame
from sqlalchemy.engine import Engine


class QuotesBtcDailyEventCommandRepository:
    """Classe para realizar o comando de consultar a API e salvar no banco de dados."""

    def __init__(
        self,
        service: QuotesBtcDailyEventService,
        engine: Engine,
        connection: ConnectionDatabase,
        table_name: str,
    ) -> None:
        """Inicializa a classe."""
        self.service = service
        self.engine = engine
        self.connection = connection
        self.table_name = table_name

    def command(self) -> DataFrame:
        """Executa o serviço e retorna DataFrame validado."""
        df: DataFrame = self.service.run()
        return df

    def save(self, df: DataFrame, mode: str = "append") -> None:
        """Salva o DataFrame no banco."""
        writer = DatabaseWriter(engine=self.engine)
        writer.save_data(df, self.table_name)
