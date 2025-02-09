import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import requests

from dotenv import dotenv_values

from src.mongodb.insert import insert_to_mongodb

settings = dotenv_values('.env')

def request_nba_league_hierarchy(access_level: str, language_code: str, format: str, api_key: str) -> dict:

    url = f"https://api.sportradar.com/nba/{access_level}/v8/{language_code}/league/hierarchy.{format}?api_key={api_key}"

    headers = {"accept" : "application/json"}

    response = requests.get(url, headers = headers)

    return response.json()


access_level = "trial"
language_code = "en"
format = "json"
api_key = settings["APIKEY"]
uri = settings["MONGOURI"]
database = "api"
collection = "nba"


if __name__ == "__main__":
    teams = request_nba_league_hierarchy(access_level=access_level, language_code=language_code, format=format, api_key=api_key)
    insert_to_mongodb(uri = uri, database=database, collection=collection, json=teams)