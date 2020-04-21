"""
API URLs.

This lists all urls under the API app.
"""
# Third-Party Libraries
from api.views import campaign_views, subscription_views, template_views
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="SPA API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "v1/swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "v1/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "v1/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path(
        "v1/subscriptions/",
        subscription_views.SubscriptionsListView.as_view(),
        name="subscriptions_list_api",
    ),
    path(
        "v1/subscription/<subscription_uuid>/",
        subscription_views.SubscriptionView.as_view(),
        name="subscriptions_get_api",
    ),
    path(
        "v1/templates/",
        template_views.TemplatesListView.as_view(),
        name="templates_list_api",
    ),
    path(
        "v1/template/<template_uuid>/",
        template_views.TemplateView.as_view(),
        name="template_get_api",
    ),
    path(
        "v1/campaigns/", campaign_views.CampaignListView.as_view(), name="campaign_list"
    ),
    path(
        "v1/campaign/<campaign_id>/",
        campaign_views.CampaignDetailView.as_view(),
        name="campaign_detail",
    ),
]
