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
from rest_framework import status

# Local Libraries
from api.models.recommendations_models import (
    RecommendationsModel,
    validate_recommendations,
)
from api.serializers.recommendations_serializers import (
    RecommendationsGetSerializer,
    RecommendationsPostSerializer,
    RecommendationsQuerySerializer,
    RecommendationsPostResponseSerializer,
)
from api.utils.db_utils import (
    delete_single,
    exists,
    get_list,
    get_single,
    save_single,
    update_single,
)


logger = logging.getLogger(__name__)


class RecommendationsListView(APIView):
    """
    This is the Recommendations List API View.

    This handles the API to get a List of Recommendations.
    """

    @swagger_auto_schema(
        query_serializer=RecommendationsQuerySerializer,
        responses={"200": RecommendationsGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="List of Recommendations",
        operation_description="This handles the API to get a List of Recommendations.",
        tags=["Recommendations"],
    )
    def get(self, request):
        """Get method."""
        serializer = RecommendationsQuerySerializer(request.GET.dict())
        parameters = serializer.data
        if not parameters:
            parameters = request.data.copy()
        recommendations_list = get_list(
            parameters,
            "recommendations",
            RecommendationsModel,
            validate_recommendations,
        )
        serializer = RecommendationsGetSerializer(recommendations_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=RecommendationsPostSerializer,
        responses={
            "201": RecommendationsPostResponseSerializer,
            "400": "Bad Request",
            "409": "CONFLICT",
        },
        security=[],
        operation_id="Create Recommendations",
        operation_description="This handles Creating a Recommendation.",
        tags=["Recommendations"],
    )
    def post(self, request, format=None):
        """Post method."""
        post_data = request.data.copy()

        if exists(
            {"name": post_data["name"]},
            "recommendation",
            RecommendationsModel,
            validate_recommendations,
        ):
            return Response(
                {"error": "Recommendation with name already exists"},
                status=status.HTTP_409_CONFLICT,
            )
        created_response = save_single(
            post_data, "recommendations", RecommendationsModel, validate_recommendations
        )
        logger.info("created response {}".format(created_response))

        if "errors" in created_response:
            return Response(created_response, status=status.HTTP_400_BAD_REQUEST)
        serializer = RecommendationsPostResponseSerializer(created_response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecommendationsView(APIView):
    """
    This is the Recommendations API View.

    This handles the API for a Recommendation with recommendations_uuid.
    """

    @swagger_auto_schema(
        responses={"200": RecommendationsGetSerializer, "400": "Bad Request"},
        security=[],
        operation_id="Get a single Recommendation",
        operation_description="This handles the API for a Get Recommendation with recommendations_uuid.",
        tags=["Recommendations"],
    )
    def get(self, request, recommendations_uuid):
        """Get method."""
        logger.debug("get recommendations uuid {}".format(recommendations_uuid))
        recommendations = get_single(
            recommendations_uuid,
            "recommendations",
            RecommendationsModel,
            validate_recommendations,
        )
        serializer = RecommendationsGetSerializer(recommendations)
        return Response(serializer.data)
