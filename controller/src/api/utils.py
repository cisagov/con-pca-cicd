"""Utils file for api."""
from django.conf import settings

# Third-Party Libraries
from database.service import Service


def db_service(collection_name, model, validate_model):
    """
    Db_service.

    This is a method for handling db connection in api.
    Might refactor this into database lib.
    """
    mongo_uri = "mongodb://{}:{}@{}:{}/".format(
        settings.DB_CONFIG["DB_USER"],
        settings.DB_CONFIG["DB_PW"],
        settings.DB_CONFIG["DB_HOST"],
        settings.DB_CONFIG["DB_PORT"],
    )

    service = Service(
        mongo_uri,
        collection_name=collection_name,
        model=model,
        model_validation=validate_model,
    )

    return service
