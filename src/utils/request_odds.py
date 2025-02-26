from typing import Dict, Optional

import requests


class RequestOdds:
    """
    Classe para interagir com a API da SportRadar.
    """

    BASE_URL = 'https://api.sportradar.com/oddscomparison-'

    def __init__(self, access_level: str, api_key: str):
        """
        Inicializa a classe de requisições.

        :param access_level: str - Nível de acesso (ex: 'trial', 'production').
        :param api_key: str - Chave de API da SportRadar.
        """
        self.access_level = access_level
        self.api_key = api_key
        self.language_code = 'en'
        self.format = 'json'
        self.headers = {'accept': 'application/json'}

    def _get(self, odds_data: str, endpoint: str) -> Optional[Dict]:
        """
        Método interno para requisições GET.

        :param endpoint: str - Endpoint da API.
        :return: Optional[Dict] - Resposta JSON ou None em caso de erro.
        """
        url = f'{self.BASE_URL}{odds_data}/{self.access_level}/v2/{self.language_code}/{endpoint}.{self.format}?api_key={self.api_key}'
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Erro na requisição: {e}')
            return None

    def get_sports(self) -> Optional[Dict]:
        return self._get('player-props', 'sports')

    def get_sports_competition(self, sport_id: str) -> Optional[Dict]:
        return self._get('player-props', f'sports/{sport_id}/competitions')

    def get_competition_schedules(self, competition_id: str) -> Optional[Dict]:
        return self._get(
            'player-props', f'competitions/{competition_id}/schedules'
        )

    def get_sport_event_player_props(
        self, sport_event_id: str
    ) -> Optional[Dict]:
        return self._get(
            'player-props', f'sport_events/{sport_event_id}/players_props'
        )

    def get_sport_event_markets(self, sport_event_id: str) -> Optional[Dict]:
        return self._get(
            'prematch', f'sport_events/{sport_event_id}/sport_event_markets'
        )
