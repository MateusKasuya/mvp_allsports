import requests

# Endpoints

# The access level of your API key
access_level = "trial"

# 2-letter code for supported languages
language_code = "en"

player_id = "8ec91366-faea-4196-bbfd-b8fab7434795"

# Format returned
format = "json"

api_key = "P2zsWC5uRpBUZCKcFODn3tir98ayYBDivgxWb9Ct"

url = f"https://api.sportradar.com/nba/{access_level}/v8/{language_code}/players/{player_id}/profile.{format}?api_key={api_key}"


headers = {"accept" : "application/json"}

response = requests.get(url, headers = headers)

print(response.json())