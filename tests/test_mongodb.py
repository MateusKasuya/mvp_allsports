from unittest.mock import MagicMock, patch

import pytest

from src.utils.mongodb import MongoDBProcess


@pytest.fixture
def mock_mongo():
    """Cria uma instância mock da classe MongoDBProcess"""
    with patch('src.utils.mongodb.MongoClient') as mock_client:
        mock_instance = mock_client.return_value
        return MongoDBProcess('mongodb://fake-uri')


def test_insert_one_success(mock_mongo):
    """Testa se a inserção de um único documento ocorre corretamente"""
    mock_mongo.client['test_db'][
        'test_collection'
    ].insert_one.return_value = MagicMock()
    result = mock_mongo.to_nosql(
        'test_db', 'test_collection', {'name': 'John Doe'}
    )
    assert 'Documento inserido com sucesso' in result


def test_insert_many_success(mock_mongo):
    """Testa se a inserção de múltiplos documentos ocorre corretamente"""
    mock_mongo.client['test_db'][
        'test_collection'
    ].insert_many.return_value = MagicMock()
    result = mock_mongo.to_nosql(
        'test_db',
        'test_collection',
        [{'name': 'John Doe'}, {'name': 'Jane Doe'}],
    )
    assert 'Documento inserido com sucesso' in result


def test_insert_failure(mock_mongo):
    """Testa erro ao inserir um único documento inválido"""
    mock_mongo.client['test_db'][
        'test_collection'
    ].insert_one.side_effect = Exception('Insert error')
    with pytest.raises(
        RuntimeError, match='Erro ao inserir no MongoDB: Insert error'
    ):
        mock_mongo.to_nosql(
            'test_db', 'test_collection', {'invalid_field': None}
        )


def test_insert_many_failure(mock_mongo):
    """Testa erro ao inserir múltiplos documentos inválidos"""
    mock_mongo.client['test_db'][
        'test_collection'
    ].insert_many.side_effect = Exception('Insert error')
    with pytest.raises(
        RuntimeError, match='Erro ao inserir no MongoDB: Insert error'
    ):
        mock_mongo.to_nosql(
            'test_db',
            'test_collection',
            [{'invalid_field': None}, {'invalid_field': None}],
        )


def test_read_success(mock_mongo):
    """Testa se a leitura retorna os documentos corretamente"""
    mock_mongo.client['test_db']['test_collection'].find.return_value = [
        {'name': 'Alice'},
        {'name': 'Bob'},
    ]
    result = mock_mongo.read_nosql('test_db', 'test_collection')
    assert result == [{'name': 'Alice'}, {'name': 'Bob'}]


def test_read_failure(mock_mongo):
    """Testa erro ao tentar fazer uma consulta"""
    mock_mongo.client['test_db'][
        'test_collection'
    ].find.side_effect = Exception('Query failed')
    with pytest.raises(
        RuntimeError, match='Erro ao ler do MongoDB: Query failed'
    ):
        mock_mongo.read_nosql('test_db', 'test_collection')


def test_close_client(mock_mongo):
    """Testa se o fechamento da conexão chama .close() corretamente"""
    mock_mongo.client.close = MagicMock()
    mock_mongo.close_client()
    mock_mongo.client.close.assert_called_once()


def test_check_if_exists_returns_true(mock_mongo):
    """Testa se check_if_exists retorna True quando um documento é encontrado"""
    mock_mongo.client['test_db'][
        'test_collection'
    ].count_documents.return_value = 1  # Simula que há um documento
    result = mock_mongo.check_if_exists(
        'test_db', 'test_collection', {'name': 'John Doe'}
    )
    assert result is True


def test_check_if_exists_returns_false(mock_mongo):
    """Testa se check_if_exists retorna False quando nenhum documento é encontrado"""
    mock_mongo.client['test_db'][
        'test_collection'
    ].count_documents.return_value = 0  # Simula que não há documentos
    result = mock_mongo.check_if_exists(
        'test_db', 'test_collection', {'name': 'Inexistente'}
    )
    assert result is False
