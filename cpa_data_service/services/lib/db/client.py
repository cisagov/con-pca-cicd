"""
This is the MongoDB Client.

This will connect to the mongodb in docker and handle trasations.
"""
# Standard Python Libraries
import datetime
import logging

# Third-Party Libraries
from pymongo import MongoClient


def connect_to_mongo(db_uri):
    """This is the basic connection method for starting mongo client."""
    client = MongoClient(db_uri)
    return client


def init_db(client, db_name):
    """This is the init method for setting up the db if not already exisiting."""
    logging.info("init database on start...")
    db = client[db_name]
    collection = db["test_collection"]
    init_data = {
        "user": "foo",
        "text": "Long text feild for testing!",
        "tags": ["one", "two", "three"],
        "date": datetime.datetime.utcnow(),
    }
    document_id = collection.insert_one(init_data).inserted_id
    found_data = collection.find_one(filter={"_id": document_id})

    logging.info("data inserted: {}".format(document_id))
    logging.info("data found: {}".format(found_data))

    collection.delete_one(filter={"_id": document_id})

    logging.info("DB collection names: {}".format(db.list_collection_names()))
    logging.info("init database on finished!")


def insert_one(db_client, collection, data):
    """This is the basic insert_one call useing the mongo client."""
    logging.info("inserting into database colleciton {}!".format(collection))
    collection = db_client[collection]
    inserted_id = collection.insert_one(data).inserted_id
    return {"id": str(inserted_id)}
