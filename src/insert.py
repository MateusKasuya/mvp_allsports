import pymongo
from pymongo import MongoClient

data = [
        {
            "customer_id": 1,
            "name": "Julian Johnston",
            "email": "rbaker@example.org",
            "phone": "(253)781-2504",
            "address": "537 Townsend Valley Apt. 824\nNew Leslie, NM 82307",
            "city": "Lake Brittney",
            "state": "North Dakota",
            "country": "Niue",
            "join_date": "2021-05-23"
        },
        {
            "customer_id": 2,
            "name": "Kevin Anderson",
            "email": "xhenson@example.net",
            "phone": "(361)858-0999",
            "address": "77028 Tammy Lodge Apt. 586\nSmithview, WI 43198",
            "city": "Lake Amy",
            "state": "Rhode Island",
            "country": "Burkina Faso",
            "join_date": "2021-06-28"
        }
]

try:
        uri = "mongodb://localhost:27017/"
        client = MongoClient(uri)

        database = client["api"]
        collection = database["nba"]

        document_list = data
        result = collection.insert_many(document_list)
        
        print(result.acknowledged)

        client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)