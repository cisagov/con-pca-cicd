"""
This is the RabbitMQ Client.

This will connect to the rabbitMQ in docker and wait for messages
"""
# Standard Python Libraries
import json
import logging

# Third-Party Libraries
from db.client import insert_one
import pika


class RabbitClient:
    """This is the client class."""

    def __init__(self, name, host, db_client):
        """This is the init def, on creation, takes client-name, amqp_url, and queue to sub to."""
        self.name = name
        self.host = host
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.db_client = db_client

    def start(self, listener_queue="", sender_queue=""):
        """Starting client."""
        logging.info("Starting client: {}".format(self.name))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=listener_queue)
        self.channel.queue_declare(queue=sender_queue)
        self.channel.basic_consume(
            queue=listener_queue, on_message_callback=self.basic_callback, auto_ack=True
        )
        logging.info("[*] Listening on queue: {}".format(listener_queue))
        logging.info(
            "[*] Sending on queue: {}. To exit press CTRL+C'".format(sender_queue)
        )

        self.channel.start_consuming()

    def stop(self):
        """Stop Client."""
        self.connection.close()
        logging.info("Stopping service {}".format(self.name))

    def basic_callback(self, ch, method, properties, body):
        """Basic callback."""
        json_data = json.loads(body)
        print(" [x] {}".format(json_data))
        self.send_db_data(json_data)

    def basic_publish_responce(self, routing_key, body):
        """Basic publish to queue."""
        logging.info("DB success! responding to queue: {}".format(body))
        self.channel.basic_publish(
            exchange="", routing_key=routing_key, body=json.dumps(body)
        )

    def send_db_data(self, json_data):
        """Sending data into db."""
        logging.info("Sending to db now: {}".format(json_data))
        responce = insert_one(
            self.db_client, json_data["collection"], json_data["data"]
        )
        self.basic_publish_responce("db_responce", responce)
