"""
Template Views.

This handles the api for all the Template urls.
"""
# Standard Python Libraries
import asyncio
import datetime
import logging
import uuid

# Third-Party Libraries
from api.models.template_models import TemplateModel, validate_template
from api.serializers.template_serializers import (
    TemplateGetSerializer,
    TemplatePostResponseSerializer,
    TemplatePostSerializer,
    TemplatePatchResponseSerializer,
    TemplatePatchSerializer,
    TemplateDeleteResponseSerializer
)
from api.utils import db_service
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class TemplatesListView(APIView):
    """
    This is the TemplatesListView APIView.

    This handles the API to get a List of Templates.
    """

    @swagger_auto_schema(
        responses={"200": TemplateGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="List of Templates",
        operation_description="This handles the API to get a List of Templates.",
    )
    def get(self, request):
        """Get method."""
        parameters = request.data.copy()
        template_list = self.__get_data(parameters)
        serializer = TemplateGetSerializer(template_list, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=TemplatePostSerializer,
        responses={"201": TemplatePostResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Create Template",
        operation_description="This handles Creating a Templates.",
    )
    def post(self, request, format=None):
        """Post method."""
        post_data = request.data.copy()
        created_response = self.__save_data(post_data)
        logging.info("created responce {}".format(created_response))
        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = TemplatePostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def __get_data(self, parameters):
        """
        Get_data private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("template", TemplateModel, validate_template)
        template_list = loop.run_until_complete(
            service.filter_list(parameters=parameters)
        )
        return template_list

    def __save_data(self, post_data):
        """
        Save_data private method.

        This method is a private method that takes in
        post_data and saves it to the db with the required feilds.
        ToDo: break out the email data into its own collection or keep flat as is.
        """
        create_timestamp = datetime.datetime.utcnow()
        current_user = "dev user"
        post_data["template_uuid"] = str(uuid.uuid4())
        post_data["created_by"] = post_data["last_updated_by"] = current_user
        post_data["cb_timestamp"] = post_data["lub_timestamp"] = create_timestamp
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("template", TemplateModel, validate_template)
        created_response = loop.run_until_complete(service.create(to_create=post_data))
        return created_response


class TemplateView(APIView):
    """
    This is the TemplateView APIView.

    This handles the API for the Get a Template with template_uuid.
    """

    @swagger_auto_schema(
        responses={"200": TemplateGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Get single Template",
        operation_description="This handles the API for the Get a Template with template_uuid.",
    )
    def get(self, request, template_uuid):
        """Get method."""
        logging.debug("get template_uuid {}".format(template_uuid))
        print("get template_uuid {}".format(template_uuid))
        template = self.__get_single(template_uuid)
        serializer = TemplateGetSerializer(template)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=TemplatePatchSerializer, 
        responses={"202": TemplatePatchResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Update and Patch single Template",
        operation_description="This handles the API for the Update Template with template_uuid.",
    )
    def patch(self, request, template_uuid):
        """Patch method."""
        logging.debug("patch template_uuid {}".format(template_uuid))
        put_data = request.data.copy()
        serialized_data = TemplatePatchSerializer(put_data)
        updated_response = self.__update_single(uuid=template_uuid, put_data=serialized_data.data)
        logging.info("created responce {}".format(updated_response))
        if "errors" in updated_response:
            return Response(updated_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = TemplatePatchResponseSerializer(updated_response)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    @swagger_auto_schema(
        responses={"200": TemplateDeleteResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Delete single Template",
        operation_description="This handles the API for the Delete of a  Template with template_uuid.",
    )
    def delete(self, request, template_uuid):
        """delete method."""
        logging.debug("delete template_uuid {}".format(template_uuid))
        delete_response = self.__delete_single(template_uuid)
        logging.info("delete responce {}".format(delete_response))
        if "errors" in delete_response:
            return Response(delete_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = TemplateDeleteResponseSerializer(delete_response)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def __get_single(self, uuid):
        """
        Get_single private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("template", TemplateModel, validate_template)
        template = loop.run_until_complete(service.get(uuid=uuid))
        return template
    
    def __update_single(self, uuid, put_data):
        """
        Update_single private method.

        This handles getting the data from the db.
        """    
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("template", TemplateModel, validate_template)

        updated_timestamp = datetime.datetime.utcnow()
        current_user = "dev user"
        put_data["template_uuid"] = uuid
        put_data["last_updated_by"] = current_user
        put_data["lub_timestamp"] = updated_timestamp

        template = loop.run_until_complete(service.get(uuid=uuid))
        template.update(put_data)
        update_response = loop.run_until_complete(service.update(template))
        if "errors" in update_response:
            return update_response
        return template
    
    def __delete_single(self, uuid):
        """
        Get_single private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("template", TemplateModel, validate_template)

        delete_response = loop.run_until_complete(service.delete(uuid=uuid))
        return delete_response
