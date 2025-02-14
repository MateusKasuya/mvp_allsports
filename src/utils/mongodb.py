from pymongo import MongoClient


class MongoDBProcess:
    """
    Classe responsável pela interação com o banco de dados MongoDB.

    A classe permite realizar operações básicas como inserção de documentos
    e leitura de dados em uma coleção do MongoDB.

    Attributes:
    ----------
    client : MongoClient
        Cliente de conexão com o MongoDB.
    db : Database
        Banco de dados selecionado no MongoDB.
    collection : Collection
        Coleção dentro do banco de dados onde as operações serão realizadas.
    """

    def __init__(self, uri: str, database: str, collection: str):
        """
        Inicializa a classe MongoDBProcess.

        Parameters:
        ----------
        uri : str
            URI de conexão do MongoDB.
        database : str
            Nome do banco de dados.
        collection : str
            Nome da coleção dentro do banco de dados.
        """
        self.client = MongoClient(uri)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def read_nosql(self, query: dict = {}):
        """
        Lê documentos de uma coleção no MongoDB.

        Parameters:
        ----------
        query : dict, opcional
            O critério de consulta para a busca dos documentos.
            O padrão é um dicionário vazio, retornando todos os documentos.

        Returns:
        -------
        list
            Lista com os documentos encontrados.

        Raises:
        ------
        Exception
            Se ocorrer um erro na consulta ao banco de dados.
        """
        try:
            results = list(self.collection.find(query))
            return results
        except Exception as e:
            raise Exception(f'An error occurred: {str(e)}')

    def to_nosql(self, json: dict):
        """
        Insere um documento na coleção MongoDB.

        Parameters:
        ----------
        json : dict
            O documento a ser inserido na coleção.

        Returns:
        -------
        str
            Mensagem de sucesso se a inserção for bem-sucedida.

        Raises:
        ------
        Exception
            Se ocorrer um erro ao tentar inserir o documento.
        """
        try:
            result = self.collection.insert_one(json)
            if result:
                return 'Inserted to MongoDB successfully'
        except Exception as e:
            raise Exception(f'The following error occurred: {e}')

    def close_client(self):
        """
        Fecha a conexão com o MongoDB.

        Libera os recursos ao fechar a conexão com o banco de dados.
        """
        self.client.close()
