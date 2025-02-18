from typing import List

from pymongo import MongoClient


class MongoDBProcess:
    """
    Classe responsável pela interação com o banco de dados MongoDB.
    Permite operações básicas como inserção, leitura e verificação de documentos.
    """

    def __init__(self, uri: str):
        """
        Inicializa a conexão com o MongoDB.

        :param uri: str - URI de conexão do MongoDB
        """
        self.client = MongoClient(uri)

    def read_nosql(
        self, database_name: str, collection_name: str, query: dict = {}
    ) -> List[dict]:
        """
        Lê documentos de uma coleção no MongoDB.

        :param database_name: str - Nome do banco de dados.
        :param collection_name: str - Nome da coleção.
        :param query: dict - Critério de consulta (opcional, padrão é vazio).
        :return: List[dict] - Lista de documentos encontrados.
        """
        try:
            collection = self.client[database_name][collection_name]
            return list(collection.find(query))
        except Exception as e:
            raise RuntimeError(f'Erro ao ler do MongoDB: {e}')

    def to_nosql(
        self, database_name: str, collection_name: str, document: dict
    ) -> str:
        """
        Insere um documento no MongoDB.

        :param database_name: str - Nome do banco de dados.
        :param collection_name: str - Nome da coleção.
        :param document: dict - Documento a ser inserido.
        :return: str - Mensagem de sucesso.
        """
        try:
            collection = self.client[database_name][collection_name]
            result = collection.insert_one(document)
            return f'Documento inserido com sucesso, ID: {result.inserted_id}'
        except Exception as e:
            raise RuntimeError(f'Erro ao inserir no MongoDB: {e}')

    def check_if_exists(
        self, database_name: str, collection_name: str, query: dict = {}
    ) -> bool:
        """
        Verifica a existência de documentos em uma coleção do MongoDB.

        :param database_name: str - Nome do banco de dados.
        :param collection_name: str - Nome da coleção.
        :param query: dict - Filtro para a verificação (opcional, padrão é vazio).
        :return: bool - True se existir pelo menos um documento, False caso contrário.
        """
        try:
            collection = self.client[database_name][collection_name]
            return (
                collection.count_documents(query) > 0
            )  # Verifica a existência de documentos corretamente
        except Exception as e:
            raise RuntimeError(f'Erro ao verificar existência no MongoDB: {e}')

    def close_client(self) -> None:
        """Fecha a conexão com o MongoDB."""
        self.client.close()
