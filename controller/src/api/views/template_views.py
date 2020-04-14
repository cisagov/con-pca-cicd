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
from api.models.template_models import TemplateModel, validate_template
from api.utils import db_service
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class TemplatesListView(APIView):
    """
    This is the TemplatesListView APIView.

    This handles the API to get a List of Templates.
    """

    def get(self, request):
        """Get method."""
        filter_map = request.data.copy()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("template", TemplateModel, validate_template)
        template_list = loop.run_until_complete(
            service.filter_list(parameters=filter_map)
        )

        return Response(template_list)

    def post(self, request, format=None):
        """Post method."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("template", TemplateModel, validate_template)
        to_create = request.data.copy()
        to_create["template_uuid"] = str(uuid.uuid4())
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


class TemplateView(APIView):
    """
    This is the TemplateView APIView.

    This handles the API for the Get a Template with template_uuid.
    """

    def get(self, request, template_uuid):
        """Get method."""
        logging.debug("get template_uuid {}".format(template_uuid))
        print("get template_uuid {}".format(template_uuid))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("template", TemplateModel, validate_template)

        template = loop.run_until_complete(service.get(uuid=template_uuid))

        return Response(template)
