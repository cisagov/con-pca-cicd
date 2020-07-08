"""
Recommendation Views.

This handles the api for all the Template urls.
"""
# Standard Python Libraries
import logging

# Third-Party Libraries
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

# Local Libraries
from api.serializers.recommendations_serializers import (
    RecommendationsGetSerializer,
    RecommendationsPostSerializer,
    RecommendationsQuerySerializer,
    RecommendationsPostResponseSerializer,
)


logger = logging.getLogger(__name__)


class RecommendationsListView(APIView):
    """
    This is the Recommendations List API View.

    This handles the API to get a List of Recommendations.
    """
    @swagger_auto_schema(
        query_serializer=RecommendationsQuerySerializer,
        responses={"200": RecommendationGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="List of Recommendations",
        operation_description="This handles the API to get a List of Recommendations.",
        tags=["Recommendations"],
    )