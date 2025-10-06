import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP")
KAFKA_KEY = os.getenv("KAFKA_KEY")
KAFKA_SECRET = os.getenv("KAFKA_SECRET")

KAFKA_TOPIC_IN_TRANSIT = os.getenv("KAFKA_TOPIC_IN_TRANSIT")
KAFKA_TOPIC_ARRIVAL = os.getenv("KAFKA_TOPIC_ARRIVAL")
KAFKA_TOPIC_CUSTOMS = os.getenv("KAFKA_TOPIC_CUSTOMS")
KAFKA_TOPIC_DELIVERED = os.getenv("KAFKA_TOPIC_DELIVERED")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
