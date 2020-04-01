"""
This is the RabbitMQ Client.

This will connect to the rabbitMQ in docker and wait for messages
"""
# Standard Python Libraries
import logging

# Third-Party Libraries
import pika


class RabbitClient:
    """This is the client class."""

    def __init__(self, name, host):
        """This is the init def, on creation, takes client-name, amqp_url, and queue to sub to."""
        self.name = name
        self.host = host
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq")
        )

    def start(self, queue=""):
        """Starting client."""
        logging.info("Starting client: {}".format(self.name))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(
            queue=queue, on_message_callback=self.basic_callback, auto_ack=True
        )
        logging.info("[*] Waiting for {}. To exit press CTRL+C'".format(queue))
        self.channel.start_consuming()

    def stop(self):
        """Stop Client."""
        self.connection.close()
        logging.info("Stopping service {}".format(self.name))

    def basic_callback(self, ch, method, properties, body):
        """Basic Service."""
        print(" [x] {}".format(body))
