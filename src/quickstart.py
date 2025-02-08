from pymongo import MongoClient

uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

try:
    database = client.get_database("api")
    movies = database.get_collection("nba")

    query = { "customer_id" : 1 }
    movie = movies.find_one(query)

    print(movie)

    client.close()

except Exception as e:
    raise Exception("Unnable to find the document due to the following error: ", e)