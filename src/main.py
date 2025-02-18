import os
import sys

from dotenv import load_dotenv

# Adiciona o diretório 'src' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.player_props_pipeline import PlayerPropsPipeline

load_dotenv()

# uri = 'mongodb://localhost:27017/'
uri = os.getenv('MONGOURI')
api_key = os.getenv('APIKEY')

if __name__ == '__main__':

    player_props = PlayerPropsPipeline(
        uri=uri,
        access_level='trial',
        api_key=api_key,
    )

    try:

        print("Verificando se 'sports' já contém dados...")
        existing_sports = player_props.check_if_exists(
            database_name='oddsplayerprops', collection_name='sports'
        )
        print(f'Documentos encontrados: {existing_sports}')

        if existing_sports == 0:
            print('Executando sports_pipeline()')
            player_props.sports_pipeline(
                database='oddsplayerprops', collection='sports'
            )
        else:
            print('Pulando sports_pipeline(), já existem dados.')

        print('Executando sports_competition_pipeline()')
        player_props.sports_competition_pipeline(
            database='oddsplayerprops',
            collection_input='sports',
            sport_name='Basketball',
            collection_output='sports_competition',
        )

    except Exception as e:
        print(f'Erro durante a execução do pipeline: {e}')

    finally:

        player_props.close_client()
