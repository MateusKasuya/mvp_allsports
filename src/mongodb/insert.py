from pymongo import MongoClient


def insert_to_mongodb(
    uri: str, database: str, collection: str, json: dict
) -> None:

    try:
        client = MongoClient(uri)

        database = client[database]
        collection = database[collection]

        document_list = [json]
        result = collection.insert_many(document_list)

        print(result.acknowledged)

        client.close()

    except Exception as e:
        raise Exception('The following error occurred: ', e)

    pass
