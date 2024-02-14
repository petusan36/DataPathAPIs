import os
import motor.motor_asyncio

# local dev
# MONGO_URL = "mongodb://root_api:api12345@localhost:27017"
# DB_NAME = "my_collections"
# db = client.get_database(DB_NAME)
# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

# on uvicorn
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client.get_database(os.environ["DB_NAME"])

movies_collection = db.get_collection("my_movies")
counters_collection = db.get_collection("counters")
