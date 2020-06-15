"""DB Utils file for api."""
# Standard Python Libraries
import asyncio
import datetime
import logging
import uuid

# Third-Party Libraries
# Models
from api.models.subscription_models import SubscriptionModel
from api.models.template_models import TemplateModel
from database.service import Service
from django.conf import settings

logger = logging.getLogger(__name__)


def __db_service(collection_name, model, validate_model):
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


def __get_service_loop(collection, model, validation_model):
    """
    Get Service Loop.

    Getting loop for asyncio and service for DB.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    service = __db_service(collection, model, validation_model)
    return service, loop


def get_list(parameters, collection, model, validation_model, fields=None):
    """
    Get_data private method.

    This handles getting the data from the db.
    """
    service, loop = __get_service_loop(collection, model, validation_model)
    document_list = loop.run_until_complete(
        service.filter_list(parameters=parameters, fields=fields)
    )
    return document_list


def save_single(post_data, collection, model, validation_model):
    """
    Save_data method.

    This method takes in
    post_data and saves it to the db with the required feilds.
    """
    service, loop = __get_service_loop(collection, model, validation_model)
    create_timestamp = datetime.datetime.utcnow()
    current_user = "dev user"
    post_data["{}_uuid".format(collection)] = str(uuid.uuid4())
    post_data["created_by"] = post_data["last_updated_by"] = current_user
    post_data["cb_timestamp"] = post_data["lub_timestamp"] = create_timestamp

    created_response = loop.run_until_complete(service.create(to_create=post_data))
    return created_response


def get_single(uuid, collection, model, validation_model):
    """
    Get_single method.

    This handles getting the data from the db.
    """
    service, loop = __get_service_loop(collection, model, validation_model)
    document = loop.run_until_complete(service.get(uuid=uuid))
    return document


def update_single(uuid, put_data, collection, model, validation_model):
    """
    Update_single method.

    This handles getting the data from the db.
    """
    service, loop = __get_service_loop(collection, model, validation_model)
    updated_timestamp = datetime.datetime.utcnow()
    current_user = "dev user"

    if isinstance(model, TemplateModel):
        put_data["template_uuid"] = uuid
    elif isinstance(model, SubscriptionModel):
        put_data["subscription_uuid"] = uuid

    put_data["last_updated_by"] = current_user
    put_data["lub_timestamp"] = updated_timestamp

    document = loop.run_until_complete(service.get(uuid=uuid))
    document.update(put_data)
    update_response = loop.run_until_complete(service.update(document))
    if "errors" in update_response:
        return update_response
    return document


def delete_single(uuid, collection, model, validation_model):
    """
    Delete_single method.

    This handles getting the data from the db.
    """
    service, loop = __get_service_loop(collection, model, validation_model)

    delete_response = loop.run_until_complete(service.delete(uuid=uuid))
    return delete_response


def get_single_subscription_webhook(campaign_id, collection, model, validation_model):
    """Get single subscription with campaign id."""
    service, loop = __get_service_loop(collection, model, validation_model)
    parameters = {"gophish_campaign_list.campaign_id": campaign_id}
    subscription_list = loop.run_until_complete(
        service.filter_list(parameters=parameters)
    )
    return next(iter(subscription_list), None)


def update_single_webhook(subscription, collection, model, validation_model):
    """Update single subscription with webhook user."""
    service, loop = __get_service_loop(collection, model, validation_model)
    put_data = {
        "last_updated_by": "webhook",
        "lub_timestamp": datetime.datetime.utcnow(),
    }
    subscription.update(put_data)
    update_response = loop.run_until_complete(service.update(subscription))
    if "errors" in update_response:
        return update_response
    return subscription
