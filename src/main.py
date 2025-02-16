from dotenv import load_dotenv
import sys
import os

# Adiciona o diretório 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.player_props_pipeline import PlayerPropsPipeline

load_dotenv()

#uri = "mongodb://localhost:27017/"
uri = os.getenv("MONGOURI")
api_key = os.getenv("APIKEY")

if __name__ == "__main__":

    player_props = PlayerPropsPipeline(uri= uri, database= "oddsplayerprops", collection= "sports", access_level= "trial", api_key= api_key)

    player_props.sports_pipeline()

    player_props.close_client()