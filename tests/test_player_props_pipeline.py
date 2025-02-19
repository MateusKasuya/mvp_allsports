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
    mock_pipeline.check_if_exists = MagicMock(
        side_effect=lambda db, coll: coll == 'sports'
    )
    mock_pipeline.read_nosql = MagicMock(
        return_value=[{'sports': [{'id': '1', 'name': 'Basketball'}]}]
    )
    mock_pipeline.get_sports_competition = MagicMock(
        return_value={'competitions': [{'id': '100', 'name': 'NBA'}]}
    )
    mock_pipeline.to_nosql = MagicMock()

    mock_pipeline.sports_competition_pipeline(
        database='test_db',
        collection_input='sports',
        sport_name='Basketball',
        collection_output='sports_competition',
    )

    mock_pipeline.get_sports_competition.assert_called_once_with(
        '1'
    )  # Verifica se foi chamado com o ID correto
    mock_pipeline.to_nosql.assert_called_once_with(
        'test_db',
        'sports_competition',
        {'competitions': [{'id': '100', 'name': 'NBA'}]},
    )


def test_sports_competition_pipeline_sport_not_found(mock_pipeline):
    """Testa se o pipeline de competições não insere dados quando o esporte não é encontrado."""
    mock_pipeline.check_if_exists = MagicMock(return_value=True)
    mock_pipeline.read_nosql = MagicMock(
        return_value=[{'sports': [{'id': '2', 'name': 'Football'}]}]
    )
    mock_pipeline.get_sports_competition = MagicMock()
    mock_pipeline.to_nosql = MagicMock()

    mock_pipeline.sports_competition_pipeline(
        database='test_db',
        collection_input='sports',
        sport_name='Basketball',
        collection_output='sports_competition',
    )

    mock_pipeline.get_sports_competition.assert_not_called()
    mock_pipeline.to_nosql.assert_not_called()


def test_competition_schedules_pipeline(mock_pipeline):
    """Testa a execução do pipeline de cronogramas de competições."""
    mock_pipeline.check_if_exists = MagicMock(
        side_effect=lambda db, coll: coll == 'sports_competition'
    )
    mock_pipeline.read_nosql = MagicMock(
        return_value=[{'competitions': [{'id': '100', 'name': 'NBA'}]}]
    )
    mock_pipeline.get_competition_schedules = MagicMock(
        return_value={'schedules': [{'game_id': '200', 'date': '2025-02-20'}]}
    )
    mock_pipeline.to_nosql = MagicMock()

    mock_pipeline.competition_schedules_pipeline(
        database='test_db',
        collection_input='sports_competition',
        competition_name='NBA',
        collection_output='competition_schedules',
    )

    mock_pipeline.get_competition_schedules.assert_called_once_with('100')
    mock_pipeline.to_nosql.assert_called_once_with(
        'test_db',
        'competition_schedules',
        {'schedules': [{'game_id': '200', 'date': '2025-02-20'}]},
    )


def test_competition_schedules_pipeline_competition_not_found(mock_pipeline):
    """Testa se o pipeline de cronogramas não insere dados quando a competição não é encontrada."""
    mock_pipeline.check_if_exists = MagicMock(return_value=True)
    mock_pipeline.read_nosql = MagicMock(
        return_value=[{'competitions': [{'id': '101', 'name': 'NFL'}]}]
    )
    mock_pipeline.get_competition_schedules = MagicMock()
    mock_pipeline.to_nosql = MagicMock()

    mock_pipeline.competition_schedules_pipeline(
        database='test_db',
        collection_input='sports_competition',
        competition_name='NBA',
        collection_output='competition_schedules',
    )

    mock_pipeline.get_competition_schedules.assert_not_called()
    mock_pipeline.to_nosql.assert_not_called()
