# validator/__init__.py
"""Pacote de validação para eventos de cotação de BTC."""

from .quotes_btc_daily_event import (
    QuotesBitcoinEventValidatorSchema as QuotesBitcoinEventValidatorSchema,
)

__all__ = ["QuotesBitcoinEventValidatorSchema"]
