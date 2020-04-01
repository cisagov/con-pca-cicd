"""
This is an example script.

It seems that it has to have THIS docstring with a summary line, a blank line
and sume more text like here. Wow.
"""
# Standard Python Libraries
import logging
from os import getenv

# Third-Party Libraries
from db.client import connect_to_mongo
from rabbit.client import RabbitClient


def load_config():
    """This loads configuration from env."""
    configs = {"AMQP_URL": getenv("AMQP_URL"), "MONGODB_URL": getenv("MONGODB_URL")}
    return configs


def main():
    """This is the Main method for starting the service."""
    service_config = load_config()

    logging.basicConfig(level=logging.getLevelName(getenv("LOG_LEVEL", "INFO")))
    logging.info("service_config {}".format(service_config))
    rabbit_client = RabbitClient("rabbit-client", service_config["AMQP_URL"])
    try:
        logging.info("Strating service {}".format("rabbit_client"))
        db_client = connect_to_mongo()
        logging.info("server version: {}".format(db_client["version"]))
        rabbit_client.start("test")
        logging.info("Strated {}".format("rabbit_client"))

    except KeyboardInterrupt:
        logging.info("Stopping service {}".format("name"))
        rabbit_client.stop()


if __name__ == "__main__":
    main()
