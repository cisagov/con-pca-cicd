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
from api.models.target_models import TargetModel, validate_target
from api.utils import db_service
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class TargetListView(APIView):
    """
    This is the TargetListView APIView.

    This handles the API to get a List of Targets.
    """

    def get(self, request):
        """Get method."""
        filter_map = request.data.copy()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("target", TargetModel, validate_target)
        target_list = loop.run_until_complete(
            service.filter_list(parameters=filter_map)
        )

        return Response(target_list)

    def post(self, request, format=None):
        """Post method."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("target", TargetModel, validate_target)
        to_create = request.data.copy()
        to_create["target_uuid"] = str(uuid.uuid4())
        # ToDo: update with current_user
        create_timestamp = datetime.datetime.utcnow()
        current_user = "dev user"
        to_create["created_by"] = to_create["last_updated_by"] = current_user
        to_create["cb_timestamp"] = to_create["lub_timestamp"] = create_timestamp
        created_responce = loop.run_until_complete(service.create(to_create=to_create))
        logging.info("created responce {}".format(created_responce))
        if "errors" in created_responce:
            return Response(created_responce, status=status.HTTP_400_BAD_REQUEST)
        return Response(created_responce, status=status.HTTP_201_CREATED)


class TargetView(APIView):
    """
    This is the TargetView APIView.

    This handles the API for the Get a Target with target_uuid.
    """

    def get(self, request, target_uuid):
        """Get method."""
        logging.debug("get target_uuid {}".format(target_uuid))
        print("get target_uuid {}".format(target_uuid))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("target", TargetModel, validate_target)

        target = loop.run_until_complete(service.get(uuid=target_uuid))

        return Response(target)
