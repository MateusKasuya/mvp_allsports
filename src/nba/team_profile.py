import requests

# Endpoints

# The access level of your API key
access_level = "trial"

# 2-letter code for supported languages
language_code = "en"

team_id = "583eca2f-fb46-11e1-82cb-f4ce4684ea4c"

# Format returned
format = "json"

api_key = "P2zsWC5uRpBUZCKcFODn3tir98ayYBDivgxWb9Ct"

url = f"https://api.sportradar.com/nba/{access_level}/v8/{language_code}/teams/{team_id}/profile.{format}?api_key={api_key}"


headers = {"accept" : "application/json"}

response = requests.get(url, headers = headers)

print(response.json())