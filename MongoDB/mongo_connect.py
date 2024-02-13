# import os
import motor.motor_asyncio

MONGO_URL = "mongodb://root_api:api12345@localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
# client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database("billboard_movie")
movies_collection = db.get_collection("my_movies")
counters_collection= db.get_collection("counters")