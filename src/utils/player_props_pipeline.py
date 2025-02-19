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
        :param collection: str - Nome da coleção onde os dados serão armazenados.
        """
        if not self.check_if_exists(database, collection):
            sports = self.get_sports()
            if sports:
                self.to_nosql(database, collection, sports)

    def _fetch_and_store(
        self,
        database: str,
        collection_input: str,
        key: str,
        value: str,
        collection_output: str,
        fetch_function,
    ):
        if self.check_if_exists(database, collection_output):
            print(
                f"[INFO] A coleção '{collection_output}' já existe no banco '{database}', pulando processamento."
            )
            return

        if not self.check_if_exists(database, collection_input):
            print(
                f"[WARNING] A coleção '{collection_input}' não foi encontrada no banco '{database}'. Verifique se os dados foram inseridos corretamente."
            )
            return

        print(
            f"[INFO] A coleção '{collection_input}' existe no banco '{database}'. Iniciando leitura dos dados..."
        )
        documents = self.read_nosql(database, collection_input)
        print(
            f"[INFO] Dados lidos da coleção '{collection_input}': {len(documents)} registros encontrados."
        )

        item_id = None
        for document in documents:
            items = document.get(key, [])
            print(f"[DEBUG] Verificando '{key}' no documento: {document}")
            for item in items:
                print(f"[DEBUG] Comparando '{item['name']}' com '{value}'...")
                if item['name'] == value:
                    item_id = item['id']
                    print(f'[SUCCESS] ID encontrado: {item_id}')
                    break
            if item_id:
                break

        if item_id is not None:
            print(f"[INFO] Buscando dados na API para o ID '{item_id}'...")
            fetched_data = fetch_function(item_id)
            print(
                f"[INFO] Dados obtidos da API: {fetched_data if fetched_data else 'Nenhum dado retornado.'}"
            )

            if fetched_data:
                print(
                    f"[INFO] Inserindo dados na coleção '{collection_output}'..."
                )
                self.to_nosql(database, collection_output, fetched_data)
                print(
                    f"[SUCCESS] Dados inseridos na coleção '{collection_output}' com sucesso!"
                )
            else:
                print(
                    f"[WARNING] Nenhum dado foi retornado da API para o ID '{item_id}'. Nenhuma inserção realizada."
                )
        else:
            print(
                f"[ERROR] Nenhum ID correspondente encontrado para '{value}' na coleção '{collection_input}'. Verifique os dados disponíveis."
            )

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
