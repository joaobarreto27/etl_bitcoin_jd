# service/__init__.py
"""Pacote de serviços para eventos diários de cotação de BTC."""

from .quotes_btc_daily_event import (
    QuotesBtcDailyEventService as QuotesBtcDailyEventService,
)

__all__ = ["QuotesBtcDailyEventService"]
