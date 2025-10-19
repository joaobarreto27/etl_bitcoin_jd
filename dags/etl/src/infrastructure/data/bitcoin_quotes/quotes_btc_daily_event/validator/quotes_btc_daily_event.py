"""Validações para o schema de eventos de cotação de BTC."""

from pydantic import BaseModel


class QuotesBitcoinEventValidatorSchema(BaseModel):
    """Schema de validação para os eventos de cotação de BTC."""

    amount: float
    base: str
    currency: str
