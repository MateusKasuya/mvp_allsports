import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from dotenv import dotenv_values

from src.api_requests.nba_requests import request_nba_league_hierarchy
from src.mongodb.insert import insert_to_mongodb

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
        'database': 'api',
        'collection': 'nba',
    },
}

if __name__ == '__main__':
    teams = request_nba_league_hierarchy(
        access_level=features['api_request']['access_level'],
        language_code=features['api_request']['language_code'],
        format=features['api_request']['format'],
        api_key=features['api_request']['api_key'],
    )
    insert_to_mongodb(
        uri=features['mongodb']['uri'],
        database=features['mongodb']['database'],
        collection=features['mongodb']['collection'],
        json=teams,
    )
