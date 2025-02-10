from pymongo import MongoClient


def query_mongodb(uri: str, database: str, collection: str, query: dict):
    client = MongoClient(uri)

    try:
        db = client[database]
        col = db[collection]

        results = list(col.find(query))

        client.close()

        # Retorna um único dicionário se houver apenas um resultado, caso contrário, retorna a lista
        if len(results) == 1:
            return results[0]
        else:
            return results

    except Exception as e:
        raise Exception(f'An error occurred: {str(e)}')
