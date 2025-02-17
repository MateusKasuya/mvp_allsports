from src.utils.mongodb import MongoDBProcess
from src.utils.request_player_props import RequestOddsPlayerProps


class PlayerPropsPipeline(MongoDBProcess, RequestOddsPlayerProps):
    def __init__(
        self,
        uri: str,
        database: str,
        collection: str,
        access_level: str,
        api_key: str,
    ):
        MongoDBProcess.__init__(self, uri, database, collection)
        RequestOddsPlayerProps.__init__(self, access_level, api_key)

    def sports_pipeline(self):

        condition = self.check_if_exists()

        if condition == False:

            sports = self.get_sports()

            self.to_nosql(sports)
