import os
import sys
from unittest.mock import MagicMock, patch

import pytest

from src.utils.mongodb import MongoDBProcess

# Adiciona o diretório raiz ao sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


@pytest.fixture
def mock_mongo():
    """Cria uma instância mock da classe MongoDBProcess"""
    with patch('src.utils.mongodb.MongoClient') as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.__getitem__.return_value = MagicMock()
        return MongoDBProcess(
            'mongodb://fake-uri', 'test_db', 'test_collection'
        )


def test_insert_success(mock_mongo):
    """Testa se a inserção ocorre corretamente"""
    mock_mongo.collection.insert_one.return_value = MagicMock()

    result = mock_mongo.to_nosql({'name': 'John Doe'})
    assert result == 'Inserted to MongoDB successfully'


def test_insert_failure(mock_mongo):
    """Testa erro ao inserir um documento inválido"""
    mock_mongo.collection.insert_one.side_effect = Exception('Insert error')

    with pytest.raises(
        Exception, match='The following error occurred: Insert error'
    ):
        mock_mongo.to_nosql({'invalid_field': None})


def test_read_success(mock_mongo):
    """Testa se a leitura retorna os documentos corretamente"""
    mock_mongo.collection.find.return_value = [
        {'name': 'Alice'},
        {'name': 'Bob'},
    ]

    result = mock_mongo.read_nosql()
    assert result == [{'name': 'Alice'}, {'name': 'Bob'}]


def test_read_failure(mock_mongo):
    """Testa erro ao tentar fazer uma consulta"""
    mock_mongo.collection.find.side_effect = Exception('Query failed')

    with pytest.raises(Exception, match='An error occurred: Query failed'):
        mock_mongo.read_nosql()


def test_close_client(mock_mongo):
    """Testa se o fechamento da conexão chama .close() corretamente"""
    mock_mongo.client.close = MagicMock()

    mock_mongo.close_client()
    mock_mongo.client.close.assert_called_once()
