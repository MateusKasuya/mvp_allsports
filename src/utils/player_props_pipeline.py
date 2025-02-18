from src.utils.mongodb import MongoDBProcess
from src.utils.request_player_props import RequestOddsPlayerProps


class PlayerPropsPipeline(MongoDBProcess, RequestOddsPlayerProps):
    """
    Pipeline para buscar e armazenar informações esportivas no MongoDB.
    """

    def __init__(self, uri: str, access_level: str, api_key: str):
        """
        Inicializa a pipeline.

        :param uri: str - URI do MongoDB.
        :param access_level: str - Nível de acesso da API.
        :param api_key: str - Chave da API.
        """
        MongoDBProcess.__init__(self, uri)
        RequestOddsPlayerProps.__init__(self, access_level, api_key)

    def sports_pipeline(self, database: str, collection: str):
        """
        Obtém e armazena esportes no MongoDB.

        :param database: str - Nome do banco de dados.
        :param collection: str - Nome da coleção.
        """
        if not self.check_if_exists(database, collection):
            sports = self.get_sports()
            if sports:
                self.to_nosql(database, collection, sports)

    def sports_competition_pipeline(
        self,
        database: str,
        collection_input: str,
        sport_name: str,
        collection_output: str,
    ):
        """
        Obtém e armazena competições de um esporte específico.

        :param database: str - Nome do banco de dados.
        :param collection_input: str - Nome da coleção de esportes.
        :param sport_name: str - Nome do esporte desejado.
        :param collection_output: str - Nome da coleção de competições.
        """
        if self.check_if_exists(database, collection_input):
            print(f'A coleção {collection_input} existe no banco {database}')
            output = self.read_nosql(database, collection_input)
            print(f'Dados lidos da coleção {collection_input}: {output}')

            sport_id = None

            for document in output:
                print(f'Documento: {document}')
                for sport in document['sports']:
                    print(f"Verificando esporte: {sport['name']}")
                    if sport['name'] == sport_name:
                        sport_id = sport['id']
                        break
                if sport_id:
                    break
            print(f'Sport ID encontrado: {sport_id}')

            if sport_id:
                sports_competition = self.get_sports_competition(sport_id)
                print(
                    f'Competições encontradas para {sport_name}: {sports_competition}'
                )
                if sports_competition:
                    self.to_nosql(
                        database, collection_output, sports_competition
                    )
                    print(
                        f'Dados inseridos na coleção {collection_output}: {sports_competition}'
                    )
