"""This is a temp test file."""
# Standard Python Libraries
import datetime
import json

# Third-Party Libraries
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="data_queue")

message = {
    "collection": "test_collection",
    "data": {
        "user": "bar",
        "text": "Long text feild for testing!",
        "tags": ["one", "two", "three"],
        "date": str(datetime.datetime.utcnow()),
    },
}

channel.basic_publish(exchange="", routing_key="data_queue", body=json.dumps(message))
print(" [x] Sent '{}'".format(message))
connection.close()
