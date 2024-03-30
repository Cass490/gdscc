from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017'  # Change this URI according to your MongoDB setup
DB_NAME = 'task_manager'  # Change this to your desired database name
client = MongoClient(MONGO_URI)
db = client[DB_NAME]