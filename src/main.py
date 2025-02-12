import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from dotenv import dotenv_values

from src.api_requests.nba_requests import (
    nba_requests_player_profile,
    request_nba_league_hierarchy,
    request_nba_team_profile,
)
from src.mongodb.extract import query_mongodb
from src.mongodb.load import load_to_mongodb

settings = dotenv_values('.env')

features = {
    'api_request': {
        'access_level': 'trial',
        'language_code': 'br',
        'format': 'json',
        'api_key': settings['APIKEY'],
    },
    'mongodb': {
        'uri': settings['MONGOURI'],
        'database': 'nba',
        'collection': ['league_hierarchy', 'team_profile', 'player_profile'],
    },
}

if __name__ == '__main__':
    # league_hierarchy = request_nba_league_hierarchy(
    #     access_level=features['api_request']['access_level'],
    #     language_code=features['api_request']['language_code'],
    #     format=features['api_request']['format'],
    #     api_key=features['api_request']['api_key'],
    # )
    # load_to_mongodb(
    #     uri=features['mongodb']['uri'],
    #     database=features['mongodb']['database'],
    #     collection=features['mongodb']['collection'][0],
    #     json=league_hierarchy,
    # )
    # teams = query_mongodb(
    #     uri=features['mongodb']['uri'],
    #     database=features['mongodb']['database'],
    #     collection=features['mongodb']['collection'][0],
    #     query={},
    # )
    # team_profile = request_nba_team_profile(
    #     teams,
    #     access_level=features['api_request']['access_level'],
    #     language_code=features['api_request']['language_code'],
    #     format=features['api_request']['format'],
    #     api_key=features['api_request']['api_key'],
    # )
    # for team in team_profile:
    #     load_to_mongodb(
    #         uri=features['mongodb']['uri'],
    #         database=features['mongodb']['database'],
    #         collection=features['mongodb']['collection'][1],
    #         json=team,
    #     )
    # players_query = query_mongodb(
    #     uri=features['mongodb']['uri'],
    #     database=features['mongodb']['database'],
    #     collection=features['mongodb']['collection'][1],
    #     query={},
    # )
    # player_profile = nba_requests_player_profile(
    #     players_query,
    #     access_level=features['api_request']['access_level'],
    #     language_code=features['api_request']['language_code'],
    #     format=features['api_request']['format'],
    #     api_key=features['api_request']['api_key'],
    # )
    # for player in player_profile:
    #     load_to_mongodb(
    #         uri=features['mongodb']['uri'],
    #         database=features['mongodb']['database'],
    #         collection=features['mongodb']['collection'][2],
    #         json=player,
    #     )
    pass
