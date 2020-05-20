"""
Template Views.

This handles the api for all the Template urls.
"""
# Standard Python Libraries
import logging

# Third-Party Libraries
from api.models.template_models import TemplateModel, validate_template
from api.serializers.template_serializers import (
    TemplateDeleteResponseSerializer,
    TemplateGetSerializer,
    TemplatePatchResponseSerializer,
    TemplatePatchSerializer,
    TemplatePostResponseSerializer,
    TemplatePostSerializer,
)
from api.utils.db_utils import (
    delete_single,
    get_list,
    get_single,
    save_single,
    update_single,
)
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
        template_list = get_list(
            parameters, "template", TemplateModel, validate_template
        )
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
        created_response = save_single(
            post_data, "template", TemplateModel, validate_template
        )
        logging.info("created responce {}".format(created_response))
        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = TemplatePostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        template = get_single(
            template_uuid, "template", TemplateModel, validate_template
        )
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
        updated_response = update_single(
            uuid=template_uuid,
            put_data=serialized_data.data,
            collection="template",
            model=TemplateModel,
            validation_model=validate_template,
        )
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
        """Delete method."""
        logging.debug("delete template_uuid {}".format(template_uuid))
        delete_response = delete_single(
            template_uuid, "template", TemplateModel, validate_template
        )
        logging.info("delete responce {}".format(delete_response))
        if "errors" in delete_response:
            return Response(delete_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = TemplateDeleteResponseSerializer(delete_response)
        return Response(serializer.data, status=status.HTTP_200_OK)
