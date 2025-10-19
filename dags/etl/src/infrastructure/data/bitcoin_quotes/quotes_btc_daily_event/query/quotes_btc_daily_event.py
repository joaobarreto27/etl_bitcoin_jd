"""Módulo para buscar dados diários de cotações de BTC diário."""

from typing import Any

from ....utils import ConnectAPI


class QuotesBtcDailyEventQueryRepository:
    """Repositório para manipulação de eventos diários de cotações de BTC."""

    def __init__(self, url: str) -> None:
        """Inicializa o repositório com a URL da API."""
        self.data_json: dict[str, Any] = {}
        self.data: dict[str, Any] = {}
        self.url = url

    def fetch(self) -> dict[str, Any]:
        """Busca os dados da API."""
        self.data_json = ConnectAPI(self.url).connect_api()
        self.data = self.data_json.get("data", {})
        return self.data
