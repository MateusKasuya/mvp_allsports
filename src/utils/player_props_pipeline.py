import time

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
        Obtém e armazena esportes no MongoDB, caso a coleção ainda não exista.

        :param database: str - Nome do banco de dados.
        :param collection: str - Nome da coleção onde os dados serão armazenados.
        """
        if not self.check_if_exists(database, collection):
            sports = self.get_sports()
            if sports:
                self.to_nosql(database, collection, sports)
                print('Sports inserido com sucesso!')
        else:
            print('Sports já existe, pulando processamento...')

    def _fetch_and_store(
        self,
        database: str,
        collection_input: str,
        key: str,
        value: str,
        collection_output: str,
        fetch_function,
    ):
        print(
            f'[DEBUG] Iniciando _fetch_and_store para {collection_output}...'
        )

        if collection_output == 'sports_competition' and self.check_if_exists(
            database, collection_output
        ):
            print(
                f"[INFO] A coleção '{collection_output}' já existe. Pulando processamento."
            )
            return

        if not self.check_if_exists(database, collection_input):
            print(
                f"[WARNING] A coleção '{collection_input}' não foi encontrada no banco '{database}'."
            )
            return

        documents = self.read_nosql(database, collection_input)
        print(
            f"[INFO] {len(documents)} registros encontrados na coleção '{collection_input}'."
        )

        item_ids = (
            [] if collection_output == 'sport_event_player_props' else None
        )

        for document in documents:
            items = document.get(key, [])

            if not isinstance(items, list):
                print(
                    f"[ERROR] Esperado uma lista em '{key}', mas encontrado: {type(items)}"
                )
                continue

            for item in items:
                if not isinstance(item, dict):
                    print(f'[ERROR] Estrutura inesperada no item: {item}')
                    continue

                if 'name' in item and item['name'] == value:
                    item_ids = item['id']
                    break
                else:
                    item_ids.append(item['sport_event']['id'])

            print(f'[DEBUG] IDs coletados: {item_ids}')

        if item_ids:
            print(f'[INFO] Buscando dados para {len(item_ids)} IDs...')

            if isinstance(item_ids, list):
                fetched_data = []
                for event_id in item_ids:
                    print(f'[DEBUG] Buscando dados para ID: {event_id}')
                    try:
                        data = fetch_function(event_id)
                        fetched_data.append(data)
                        time.sleep(10)
                    except Exception as e:
                        print(
                            f'[ERROR] Erro ao buscar dados para {event_id}: {e}'
                        )
            else:
                fetched_data = fetch_function(item_ids)

            if fetched_data:

                self.to_nosql(database, collection_output, fetched_data)
                print(
                    f"[SUCCESS] Dados inseridos na coleção '{collection_output}' com sucesso!"
                )
            else:
                print(
                    f'[WARNING] Nenhum dado retornado da API para os IDs coletados.'
                )
        else:
            print(
                f"[ERROR] Nenhum ID correspondente encontrado para '{value}' na coleção '{collection_input}'."
            )

        time.sleep(10)

    def sports_competition_pipeline(
        self,
        database: str,
        collection_input: str,
        sport_name: str,
        collection_output: str,
    ):
        """
        Obtém e armazena competições de um esporte específico no MongoDB.

        :param database: str - Nome do banco de dados.
        :param collection_input: str - Nome da coleção contendo os esportes.
        :param sport_name: str - Nome do esporte desejado.
        :param collection_output: str - Nome da coleção onde os dados de competições serão armazenados.
        """
        self._fetch_and_store(
            database,
            collection_input,
            'sports',
            sport_name,
            collection_output,
            self.get_sports_competition,
        )

    def competition_schedules_pipeline(
        self,
        database: str,
        collection_input: str,
        competition_name: str,
        collection_output: str,
    ):
        """
        Obtém e armazena os cronogramas de uma competição específica no MongoDB.

        :param database: str - Nome do banco de dados.
        :param collection_input: str - Nome da coleção contendo as competições.
        :param competition_name: str - Nome da competição desejada.
        :param collection_output: str - Nome da coleção onde os dados do cronograma serão armazenados.
        """
        self._fetch_and_store(
            database,
            collection_input,
            'competitions',
            competition_name,
            collection_output,
            self.get_competition_schedules,
        )

    def sport_event_player_props_pipeline(
        self, database: str, collection_input: str, collection_output: str
    ):
        """
        Obtém e armazena informações de eventos esportivos de jogadores no MongoDB.
        """
        print(
            f'[DEBUG] Chamando sport_event_player_props_pipeline com {database}, {collection_input}, {collection_output}'
        )
        self._fetch_and_store(
            database,
            collection_input,
            'schedules',
            None,
            collection_output,
            self.get_sport_event_player_props,
        )
