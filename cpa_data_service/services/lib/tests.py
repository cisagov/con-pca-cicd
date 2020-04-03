"""This is a temp test file."""
# Third-Party Libraries
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="test")

channel.basic_publish(exchange="", routing_key="test", body="Hello World!")
print(" [x] Sent 'Hello World!'")
connection.close()
