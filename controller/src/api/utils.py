"""Utils file for api."""

# Third-Party Libraries
from config.settings import DB_CONFIG
from database.service import Service


def db_service(collection_name, model, validate_model):
    """
    Db_service.

    This is a method for handling db connection in api.
    Might refactor this into database lib.
    """
    mongo_uri = "mongodb://{}:{}@{}:{}/".format(
        DB_CONFIG["DB_USER"],
        DB_CONFIG["DB_PW"],
        DB_CONFIG["DB_HOST"],
        DB_CONFIG["DB_PORT"],
    )

    service = Service(
        mongo_uri,
        collection_name=collection_name,
        model=model,
        model_validation=validate_model,
    )

    return service
