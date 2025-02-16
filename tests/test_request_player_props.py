import pytest
import requests
import requests_mock

from utils.request_player_props import RequestOddsPlayerProps

API_KEY = 'fake_api_key'
ACCESS_LEVEL = 'trial'


@pytest.fixture
def api_client():
    """Cria uma instância da classe OddsPlayerProps para os testes."""
    return RequestOddsPlayerProps(ACCESS_LEVEL, API_KEY)


def test_get_sports(api_client):
    """Testa se o método get_sports retorna os esportes corretamente."""
    with requests_mock.Mocker() as m:
        fake_response = {'sports': [{'id': '1', 'name': 'Football'}]}
        m.get(
            f'{api_client.BASE_URL}/{ACCESS_LEVEL}/v2/en/sports.json?api_key={API_KEY}',
            json=fake_response,
            status_code=200,
        )
        response = api_client.get_sports()
        assert response == fake_response


def test_get_sports_competition(api_client):
    """Testa se o método get_sports_competition retorna competições corretamente."""
    sport_id = '1'
    with requests_mock.Mocker() as m:
        fake_response = {
            'competitions': [{'id': '100', 'name': 'Premier League'}]
        }
        m.get(
            f'{api_client.BASE_URL}/{ACCESS_LEVEL}/v2/en/sports/{sport_id}/competitions.json?api_key={API_KEY}',
            json=fake_response,
            status_code=200,
        )
        response = api_client.get_sports_competition(sport_id)
        assert response == fake_response


def test_get_competition_schedules(api_client):
    """Testa se o método get_competition_schedules retorna os cronogramas corretamente."""
    competition_id = '100'
    with requests_mock.Mocker() as m:
        fake_response = {
            'schedules': [{'event_id': '500', 'date': '2024-02-20'}]
        }
        m.get(
            f'{api_client.BASE_URL}/{ACCESS_LEVEL}/v2/en/competitions/{competition_id}/schedules.json?api_key={API_KEY}',
            json=fake_response,
            status_code=200,
        )
        response = api_client.get_competition_schedules(competition_id)
        assert response == fake_response


def test_get_sport_event_player_props(api_client):
    """Testa se o método get_sport_event_player_props retorna as probabilidades corretamente."""
    sport_event_id = '500'
    with requests_mock.Mocker() as m:
        fake_response = {
            'players_props': [{'player': 'John Doe', 'odds': 2.5}]
        }
        m.get(
            f'{api_client.BASE_URL}/{ACCESS_LEVEL}/v2/en/sport_events/{sport_event_id}/players_props.json?api_key={API_KEY}',
            json=fake_response,
            status_code=200,
        )
        response = api_client.get_sport_event_player_props(sport_event_id)
        assert response == fake_response


def test_request_error_handling(api_client):
    """Testa se a classe lida corretamente com erros de requisição."""
    with requests_mock.Mocker() as m:
        m.get(
            f'{api_client.BASE_URL}/{ACCESS_LEVEL}/v2/en/sports.json?api_key={API_KEY}',
            status_code=500,  # Simula um erro no servidor
        )
        response = api_client.get_sports()
        assert response is None  # O método deve retornar None em caso de erro
