# query/__init__.py
"""Pacote de comandos para eventos diários de cotação de BTC."""

from .quotes_btc_daily_event import (
    QuotesBtcDailyEventQueryRepository as QuotesBtcDailyEventQueryRepository,
)

__all__ = ["QuotesBtcDailyEventQueryRepository"]
