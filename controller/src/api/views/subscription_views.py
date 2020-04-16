"""
This is the main views for api.

This handles api views
"""
# Standard Python Libraries
import asyncio
import datetime
import logging
import uuid

# Third-Party Libraries
from api.models.subscription_models import SubscriptionModel, validate_subscription
from api.utils import db_service
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class SubscriptionsListView(APIView):
    """
    This is the SubscriptionsListView APIView.

    This handles the API to get a List of Subscriptions.
    """

    def get(self, request):
        """Get method."""
        parameters = request.data.copy()
        subscription_list = self.__get_data(parameters)
        return Response(subscription_list)

    def post(self, request, format=None):
        """
        Post method.

        ToDo:
        Create gophish calls and data here before saving to db.
        post_data["gophish_campaign_list"] = [{
            "template_email": "",
            "template_landing_page": "",
            "start_date": "2020-03-19T09:30:25",
            "target_email_list": [
                {"group": "name", "emails": [....]
            ],
            }
            ]
        """
        post_data = request.data.copy()
        created_responce = self.__save_data(post_data)
        print("created responce: {}".format(created_responce))
        if "errors" in created_responce:
            return Response(created_responce, status=status.HTTP_400_BAD_REQUEST)
        return Response(created_responce, status=status.HTTP_201_CREATED)

    def __get_data(self, parameters):
        """
        Get_data private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)
        subscription_list = loop.run_until_complete(
            service.filter_list(parameters=parameters)
        )
        return subscription_list

    def __save_data(self, post_data):
        """
        Save_data private method.

        This method is a private method that takes in
        post_data and saves it to the db with the required feilds.
        ToDo: break out the email data into its own collection or keep flat as is.
        """
        print("post object: {}".format(post_data))
        create_timestamp = datetime.datetime.utcnow()
        current_user = "dev user"
        post_data["subscription_uuid"] = str(uuid.uuid4())
        post_data["created_by"] = post_data["last_updated_by"] = current_user
        post_data["cb_timestamp"] = post_data["lub_timestamp"] = create_timestamp
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)
        created_responce = loop.run_until_complete(service.create(to_create=post_data))
        return created_responce


class SubscriptionView(APIView):
    """
    This is the SubscriptionsView APIView.

    This handles the API for the Get a Substription with subscription_uuid.
    """

    def get(self, request, subscription_uuid):
        """Get method."""
        print("get subscription_uuid {}".format(subscription_uuid))
        subscription = self.__get_single(subscription_uuid)

        return Response(subscription)

    def __get_single(self, subscription_uuid):
        """
        Get_single private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("subscription", SubscriptionModel, validate_subscription)
        subscription = loop.run_until_complete(service.get(uuid=subscription_uuid))
        return subscription
