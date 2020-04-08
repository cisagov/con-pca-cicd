"""
This is an example stript.

Here is an example on how to run and call the db.
This shows the create, filter, and use of filter of
demo objects in a demo collelction.

TODO: Setup Mocks and not rely on db conneciton.

"""
# Standard Python Libraries
import asyncio
from datetime import datetime
import json
import logging
import os
import unittest
import uuid

# Third-Party Libraries
from service import Service
from test_validators import DemoModel, validate_demo


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
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_USER": os.getenv("DB_USER"),
            "DB_PW": os.getenv("DB_PW"),
            "DB_PORT": os.getenv("DB_PORT"),
        }

    return configs


class TestStringMethods(unittest.TestCase):
    """Unittest TestCase Class."""

    @classmethod
    def setUpClass(cls):
        """
        SetUpClass.

        Taking in env from local json and setting up database connection.
        This should be mocked.
        """
        cls.service_config = load_config()
        cls.mongo_uri = "mongodb://{}:{}@{}:{}/".format(
            cls.service_config["DB_USER"],
            cls.service_config["DB_PW"],
            cls.service_config["DB_HOST"],
            cls.service_config["DB_PORT"],
        )

        logging.basicConfig(level=logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")))
        logging.info("service_config {}".format(cls.service_config))

        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)

        cls.demo_service = Service(
            cls.mongo_uri,
            collection_name="demo",
            model=DemoModel,
            model_validation=validate_demo,
        )

    def test_create(self):
        """
        Test Case: Create.

        This is to test the creation method on service.
        """
        demo_id = str(uuid.uuid4())
        self.to_create = {
            "demo_uuid": demo_id,
            "name": "demo 1",
            "enum_type": "initial",
            "record_tstamp": datetime.utcnow(),
            "method_of_record_creation": "CLI",
            "last_updated_by": "test user 1",
        }

        self.loop.run_until_complete(self.demo_service.create(to_create=self.to_create))
        created = self.loop.run_until_complete(self.demo_service.get(uuid=demo_id))

        self.assertEqual(created["demo_uuid"], demo_id)

        logging.info("created {}".format(created))
        delteted = self.loop.run_until_complete(self.demo_service.delete(uuid=demo_id))
        logging.info("delteted {}".format(delteted))

    def test_filter_empty(self):
        """
        Test Case: Filter.

        This is to test the filter method on service.
        """
        self.assertEqual("foo".upper(), "FOO")

    def test_get(self):
        """
        Test Case: Get.

        This is to test the get method on service.
        """
        self.assertEqual("foo".upper(), "FOO")

    def test_count(self):
        """
        Test Case: Count.

        This is to test the count method on service.
        """
        self.assertEqual("foo".upper(), "FOO")

    def test_update(self):
        """
        Test Case: Update.

        This is to test the update method on service.
        """
        self.assertEqual("foo".upper(), "FOO")

    def test_delete(self):
        """
        Test Case: Delete.

        This is to test the delete method on service.
        """
        self.assertEqual("foo".upper(), "FOO")


if __name__ == "__main__":
    unittest.main()
