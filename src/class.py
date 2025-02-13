import requests
from pymongo import MongoClient

class OddSportsPipeline:
    def __init__(self, mongo_uri: str, database: str, collection: str):
        self.client = MongoClient(mongo_uri)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def sports_request(
        self, access_level: str = "trial", language_code: str = "en", format: str = "json",
        api_key: str = "P2zsWC5uRpBUZCKcFODn3tir98ayYBDivgxWb9Ct"
    ) -> dict:
        url = f"https://api.sportradar.com/oddscomparison-player-props/{access_level}/v2/{language_code}/sports.{format}?api_key={api_key}"
        
        try:
            response = requests.get(url, headers={"accept": "application/json"})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return {}

    def load_to_mongodb(self, data: dict) -> None:
        """Insere os dados no MongoDB"""
        try:
            if data:
                result = self.collection.insert_one(data)
                print(f"Documento inserido com sucesso: {result.inserted_id}")
            else:
                print("Nenhum dado válido para inserir.")
        except Exception as e:
            print(f"Erro ao inserir no MongoDB: {e}")

    def close_connection(self):
        """Fecha a conexão com o MongoDB"""
        self.client.close()
