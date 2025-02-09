import requests


def request_nba_league_hierarchy(
    access_level: str, language_code: str, format: str, api_key: str
) -> dict:

    url = f'https://api.sportradar.com/nba/{access_level}/v8/{language_code}/league/hierarchy.{format}?api_key={api_key}'

    headers = {'accept': 'application/json'}

    response = requests.get(url, headers=headers)

    return response.json()
