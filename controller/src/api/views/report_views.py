"""
Reports Views.

This handles the api for all the Reports urls.
"""
# Standard Python Libraries
import logging

# Third-Party Libraries
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ReportsView(APIView):
    """
    This is the ReportsView API Endpoint.

    This handles the API a Get .
    """
