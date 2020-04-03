"""
This is an example script.

It seems that it has to have THIS docstring with a summary line, a blank line
and sume more text like here. Wow.
"""
# Standard Python Libraries
import json
import logging
import os

# Third-Party Libraries
from db.client import connect_to_mongo, init_db
from rabbit.client import RabbitClient


def load_config():
    """This loads configuration from env."""
    if os.getenv("RABBIT_HOST") is None:
        project_root = os.path.abspath(__file__).rsplit("/", 2)[0]
        config_file = os.getenv(
            "CPA_DATA_CONFIG_FILE",
            os.path.join(project_root, "deployment/local_config.json"),
        )
        with open(config_file, "r") as f:
            configs = json.load(f)

    else:
        configs = {
            "rabbit_host": os.getenv("RABBIT_HOST"),
            "mongo_uri": os.getenv("MONGO_URI"),
        }

    return configs


def main():
    """This is the Main method for starting the service."""
    service_config = load_config()

    logging.basicConfig(level=logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")))
    logging.info("service_config {}".format(service_config))

    db_client = connect_to_mongo(db_uri=service_config["mongo_uri"])
    init_db(db_client, "cpa_data_dev")

    rabbit_client = RabbitClient(
        "rabbit-client", service_config["rabbit_host"], db_client["cpa_data_dev"]
    )

    try:
        logging.info("Strating service {}".format("rabbit_client"))
        logging.info("server version: {}".format(db_client["version"]))
        logging.info("test db client: {}".format(db_client.list_database_names()))
        rabbit_client.start(listener_queue="data_queue", sender_queue="db_responce")
        logging.info("Strated {}".format("rabbit_client"))

    except KeyboardInterrupt:
        logging.info("Stopping service {}".format("name"))
        rabbit_client.stop()


if __name__ == "__main__":
    main()
