"""
This is the MongoDB Client.

This will connect to the mongodb in docker and handle trasations.
"""
# Third-Party Libraries
from pymongo import MongoClient


def connect_to_mongo():
    """This is the basic connection method for starting mongo client."""
    client = MongoClient("localhost", 27017)
    return client
