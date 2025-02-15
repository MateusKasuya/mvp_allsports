from typing import Dict, Optional

import requests


class OddsPlayerProps:
    """
    Classe para interagir com a API da SportRadar para obter informações sobre esportes,
    competições, cronogramas e probabilidades de jogadores.

    Args:
        access_level (str): Nível de acesso da API (por exemplo, 'trial', 'production').
        api_key (str): Chave de API fornecida pela SportRadar.
    """

    BASE_URL = 'https://api.sportradar.com/oddscomparison-player-props'

    def __init__(self, access_level: str, api_key: str):
        self.access_level = access_level
        self.language_code = 'en'
        self.format = 'json'
        self.api_key = api_key
        self.headers = {'accept': 'application/json'}

    def _get(self, endpoint: str) -> Optional[Dict]:
        """
        Método interno para realizar requisições GET à API.

        Args:
            endpoint (str): O endpoint da API a ser acessado.

        Returns:
            Optional[Dict]: Resposta da API em formato JSON, ou None em caso de erro.
        """
        url = f'{self.BASE_URL}/{self.access_level}/v2/{self.language_code}/{endpoint}.{self.format}?api_key={self.api_key}'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Lança um erro se o status não for 2xx
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Erro ao acessar {url}: {e}')
            return None

    def get_sports(self) -> Optional[Dict]:
        """
        Obtém a lista de esportes disponíveis na API.

        Returns:
            Optional[Dict]: Dicionário contendo os esportes disponíveis, ou None em caso de erro.
        """
        return self._get('sports')

    def get_sports_competition(self, sport_id: str) -> Optional[Dict]:
        """
        Obtém as competições de um determinado esporte.

        Args:
            sport_id (str): ID do esporte.

        Returns:
            Optional[Dict]: Dicionário contendo as competições do esporte informado, ou None em caso de erro.
        """
        return self._get(f'sports/{sport_id}/competitions')

    def get_competition_schedules(self, competition_id: str) -> Optional[Dict]:
        """
        Obtém a programação de uma competição específica.

        Args:
            competition_id (str): ID da competição.

        Returns:
            Optional[Dict]: Dicionário contendo o cronograma da competição, ou None em caso de erro.
        """
        return self._get(f'competitions/{competition_id}/schedules')

    def get_sport_event_player_props(
        self, sport_event_id: str
    ) -> Optional[Dict]:
        """
        Obtém as probabilidades de jogadores para um evento esportivo específico.

        Args:
            sport_event_id (str): ID do evento esportivo.

        Returns:
            Optional[Dict]: Dicionário contendo as probabilidades dos jogadores, ou None em caso de erro.
        """
        return self._get(f'sport_events/{sport_event_id}/players_props')
