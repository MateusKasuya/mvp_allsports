from unittest.mock import MagicMock, patch

import pytest

from src.utils.player_props_pipeline import PlayerPropsPipeline


@pytest.fixture
def mock_pipeline():
    """
    Cria uma instância mock da classe PlayerPropsPipeline.
    """
    with patch(
        'src.utils.mongodb.MongoDBProcess.__init__', return_value=None
    ), patch(
        'src.utils.request_player_props.RequestOddsPlayerProps.__init__',
        return_value=None,
    ):
        pipeline = PlayerPropsPipeline(
            uri='mongodb://fake-uri',
            access_level='trial',
            api_key='fake-api-key',
        )
        pipeline.client = MagicMock()  # Mock do cliente MongoDB
        pipeline.read_nosql = MagicMock(return_value=[])
        return pipeline


def test_sports_pipeline(mock_pipeline):
    """Testa a execução do pipeline de esportes."""
    mock_pipeline.check_if_exists = MagicMock(return_value=False)
    mock_pipeline.get_sports = MagicMock(
        return_value={'sports': [{'id': '1', 'name': 'Basketball'}]}
    )
    mock_pipeline.to_nosql = MagicMock()

    mock_pipeline.sports_pipeline(database='test_db', collection='sports')

    mock_pipeline.get_sports.assert_called_once()
    mock_pipeline.to_nosql.assert_called_once_with(
        'test_db', 'sports', {'sports': [{'id': '1', 'name': 'Basketball'}]}
    )


def test_sports_pipeline_already_exists(mock_pipeline):
    """Testa se o pipeline de esportes não insere dados se a coleção já existir."""
    mock_pipeline.check_if_exists = MagicMock(return_value=True)
    mock_pipeline.get_sports = MagicMock()
    mock_pipeline.to_nosql = MagicMock()

    mock_pipeline.sports_pipeline(database='test_db', collection='sports')

    mock_pipeline.get_sports.assert_not_called()
    mock_pipeline.to_nosql.assert_not_called()


def test_sports_competition_pipeline(mock_pipeline):
    """Testa a execução do pipeline de competições esportivas."""
    mock_pipeline._fetch_and_store = MagicMock()
    mock_pipeline.get_sports_competition = MagicMock(
        return_value=[{'id': '100', 'name': 'NBA'}]
    )

    mock_pipeline.sports_competition_pipeline(
        database='test_db',
        collection_input='sports',
        sport_name='Basketball',
        collection_output='sports_competition',
    )

    mock_pipeline._fetch_and_store.assert_called_once_with(
        'test_db',
        'sports',
        'sports',
        'Basketball',
        'sports_competition',
        mock_pipeline.get_sports_competition,
    )


def test_competition_schedules_pipeline(mock_pipeline):
    """Testa a execução do pipeline de cronogramas de competições."""
    mock_pipeline._fetch_and_store = MagicMock()
    mock_pipeline.get_competition_schedules = MagicMock(
        return_value=[{'id': '200', 'name': 'NBA Finals'}]
    )

    mock_pipeline.competition_schedules_pipeline(
        database='test_db',
        collection_input='sports_competition',
        competition_name='NBA',
        collection_output='competition_schedules',
    )

    mock_pipeline._fetch_and_store.assert_called_once_with(
        'test_db',
        'sports_competition',
        'competitions',
        'NBA',
        'competition_schedules',
        mock_pipeline.get_competition_schedules,
    )


def test_sport_event_player_props_pipeline(mock_pipeline):
    """Testa a execução do pipeline de eventos esportivos de jogadores."""
    mock_pipeline._fetch_and_store = MagicMock()
    mock_pipeline.get_sport_event_player_props = MagicMock(
        return_value=[{'id': '300', 'event': 'NBA Game'}]
    )

    mock_pipeline.sport_event_player_props_pipeline(
        database='test_db',
        collection_input='schedules',
        collection_output='sport_event_player_props',
    )

    mock_pipeline._fetch_and_store.assert_called_once_with(
        'test_db',
        'schedules',
        'schedules',
        None,
        'sport_event_player_props',
        mock_pipeline.get_sport_event_player_props,
    )
