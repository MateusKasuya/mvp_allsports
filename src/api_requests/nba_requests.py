import time

import requests


def request_nba_league_hierarchy(
    access_level: str, language_code: str, format: str, api_key: str
) -> dict:

    url = f'https://api.sportradar.com/nba/{access_level}/v8/{language_code}/league/hierarchy.{format}?api_key={api_key}'

    headers = {'accept': 'application/json'}

    response = requests.get(url, headers=headers)

    return response.json()


def request_nba_team_profile(
    dict_team: dict,
    access_level: str,
    language_code: str,
    format: str,
    api_key: str,
):

    team_ids = [
        team['id']
        for conference in dict_team['conferences']
        for division in conference['divisions']
        for team in division['teams']
    ]

    list_of_teams = []

    for team_id in team_ids:

        url = f'https://api.sportradar.com/nba/{access_level}/v8/{language_code}/teams/{team_id}/profile.{format}?api_key={api_key}'

        headers = {'accept': 'application/json'}

        response = requests.get(url, headers=headers)

        data = response.json()

        list_of_teams.append(data)

        time.sleep(5)

    return list_of_teams
