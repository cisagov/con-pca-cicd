"""
Customer Views.

This handles the api for all the Template urls.
"""
# Standard Python Libraries
import asyncio
import datetime
import logging
import uuid

# Third-Party Libraries
from api.models.customer_models import CustomerModel, validate_customer
from api.serializers.customer_serializers import (
    CustomerGetSerializer,
    CustomerPostResponseSerializer,
    CustomerPostSerializer,
    CustomerPatchResponseSerializer,
    CustomerPatchSerializer
)
from api.utils import db_service
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class CustomerListView(APIView):
    """
    This is the CustomerListView APIView.

    This handles the API to get a List of Templates.
    """

    @swagger_auto_schema(
        responses={"200": CustomerGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="List of Customers",
        operation_description="This handles the API to get a List of Customers.",
    )
    def get(self, request):
        """Get method."""
        parameters = request.data.copy()
        customer_list = self.__get_data(parameters)
        serializer = CustomerGetSerializer(customer_list, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CustomerPostSerializer,
        responses={"201": CustomerPostResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Create Customer",
        operation_description="This handles Creating a Customers.",
    )
    def post(self, request, format=None):
        """Post method."""
        post_data = request.data.copy()
        created_response = self.__save_data(post_data)
        logging.info("created responce {}".format(created_response))
        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerPostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def __get_data(self, parameters):
        """
        Get_data private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("customer", CustomerModel, validate_customer)
        customer_list = loop.run_until_complete(
            service.filter_list(parameters=parameters)
        )
        return customer_list

    def __save_data(self, post_data):
        """
        Save_data private method.

        This method is a private method that takes in
        post_data and saves it to the db with the required feilds.
        ToDo: break out the email data into its own collection or keep flat as is.
        """
        create_timestamp = datetime.datetime.utcnow()
        current_user = "dev user"
        post_data["customer_uuid"] = str(uuid.uuid4())
        post_data["created_by"] = post_data["last_updated_by"] = current_user
        post_data["cb_timestamp"] = post_data["lub_timestamp"] = create_timestamp
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("customer", CustomerModel, validate_customer)
        created_response = loop.run_until_complete(service.create(to_create=post_data))
        return created_response


class CustomerView(APIView):
    """
    This is the CustomerView APIView.

    This handles the API for the Get a Customer with customer_uuid.
    """

    @swagger_auto_schema(
        responses={"200": CustomerGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Get single Customer",
        operation_description="This handles the API for the Get a Customer with customer_uuid.",
    )
    def get(self, request, customer_uuid):
        """Get method."""
        logging.debug("get customer_uuid {}".format(customer_uuid))
        customer = self.__get_single(customer_uuid)
        serializer = CustomerGetSerializer(customer)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CustomerPatchSerializer, 
        responses={"202": CustomerPatchResponseSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Update and Patch single Customer",
        operation_description="This handles the API for the Update Customer with customer_uuid.",
    )
    def put(self, request, customer_uuid):
        """Put method."""
        logging.debug("get customer_uuid {}".format(customer_uuid))
        put_data = request.data.copy()
        serialized_data = CustomerPatchSerializer(put_data)
        updated_response = self.__update_single(customer_uuid, serialized_data.data)
        logging.info("created responce {}".format(updated_response))
        if "errors" in updated_response:
            return Response(updated_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerPatchResponseSerializer(updated_response)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def __get_single(self, customer_uuid):
        """
        Get_single private method.

        This handles getting the data from the db.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("customer", CustomerModel, validate_customer)
        customer = loop.run_until_complete(service.get(uuid=customer_uuid))
        return customer
    
    def __update_single(self, uuid, put_data):
        """
        Update_single private method.

        This handles getting the data from the db.
        """            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        service = db_service("customer", CustomerModel, validate_customer)

        updated_timestamp = datetime.datetime.utcnow()
        current_user = "dev user"
        put_data["customer_uuid"] = uuid
        put_data["last_updated_by"] = current_user
        put_data["lub_timestamp"] = updated_timestamp

        customer = loop.run_until_complete(service.get(uuid=uuid))
        customer.update(put_data)
        update_response = loop.run_until_complete(service.update(customer))
        if "errors" in update_response:
            return update_response
        return customer
