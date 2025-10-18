"""Módulo responsável por conectar na API."""

from typing import Any

import requests


class ConnectAPI:
    """Gerencia conexão com a API."""

    def __init__(self, url: str) -> None:
        """Inicializa a conexão com a API.

        Args:
            url (str): URL base da API.

        """
        self.url: str = url
        self.data_json: dict[str, Any] = {}

    def connect_api(
        self,
    ) -> dict[str, Any]:
        """Conecta a uma API com autenticação flexível.

        Args:
            self.

        Returns:
            dict[str, Any]: Resposta JSON da API.

        Raises:
            ValueError: Se os parâmetros de autenticação forem inválidos
            ou a requisição falhar.
        """
        response = requests.get(url=self.url, timeout=10)
        if response.status_code == 200:
            self.data_json = response.json()
        else:
            raise ValueError("Connection error: Please try again.")
        return self.data_json
