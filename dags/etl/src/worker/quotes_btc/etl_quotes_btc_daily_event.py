"""Worker responsável por executar o ETL diário de cotação de BTC."""

from datetime import datetime

from infrastructure.data.bitcoin_data.quotes_btc_daily_event.command import (
    QuotesBtcDailyEventCommandRepository,
)
from infrastructure.data.bitcoin_quotes.quotes_btc_daily_event.query import (
    QuotesBtcDailyEventQueryRepository,
)
from infrastructure.data.bitcoin_quotes.quotes_btc_daily_event.service import (
    QuotesBtcDailyEventService,
)
from infrastructure.data.utils import ConnectionDatabase


def main() -> None:
    """Executa todo o ETL."""
    USE_SQLITE = False

    connection = ConnectionDatabase(
        sgbd_name="sqlite" if USE_SQLITE else "postgresql",
        environment="dev" if USE_SQLITE else "dev",
        db_name=("etl_bitcoin_jd" if USE_SQLITE else "etl_bitcoin_jd"),
    )

    engine = connection.initialize_engine()

    query_repository = QuotesBtcDailyEventQueryRepository(
        "https://api.coinbase.com/v2/prices/spot"
    )

    service = QuotesBtcDailyEventService(query_repository)

    # 5. CommandRepository (roda ETL + salva no banco)
    command = QuotesBtcDailyEventCommandRepository(
        service=service,
        connection=connection,
        engine=engine,  # type:ignore
        table_name="quotes_btc_daily_event",
    )

    df_clean = command.command()
    df_clean["extract_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(df_clean.head(5))
    command.save(df_clean)


if __name__ == "__main__":
    main()
