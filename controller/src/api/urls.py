"""
API URLs.

This lists all urls under the API app.
"""
# Third-Party Libraries
from api.views import (
    campaign_views,
    customer_views,
    report_views,
    subscription_views,
    template_views,
    sendingprofile_views,
    webhook_views,
)
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Con-PCA API",
        default_version="v1",
        description="""This is the API documentation for Con-PCA.
        This was created to define all API calls and repsonses.""",
        terms_of_service="https://github.com/cisagov/cpa/blob/develop/LICENSE",
        contact=openapi.Contact(email="peter.mercado255@gmail.com"),
        license=openapi.License(name="Public Domain"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "v1/swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "v1/swagger.yaml", schema_view.without_ui(cache_timeout=0), name="schema-yaml"
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
        "v1/subscription/customer/<customer_uuid>/",
        subscription_views.SubscriptionsCustomerListView.as_view(),
        name="subscriptions_customer_get_api",
    ),
    path(
        "v1/subscription/template/<template_uuid>/",
        subscription_views.SubscriptionsTemplateListView.as_view(),
        name="subscriptions_template_get_api",
    ),
    path(
        "v1/subscription/stop/<subscription_uuid>/",
        subscription_views.SubscriptionStopView.as_view(),
        name="subscription_stop_api",
    ),
    path(
        "v1/reports/<subscription_uuid>/",
        report_views.ReportsView.as_view(),
        name="reports_get_api",
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
        "v1/template/stop/<template_uuid>/",
        template_views.TemplateStopView.as_view(),
        name="template_stop_api",
    ),
    path(
        "v1/campaigns/", campaign_views.CampaignListView.as_view(), name="campaign_list"
    ),
    path(
        "v1/campaign/<campaign_id>/",
        campaign_views.CampaignDetailView.as_view(),
        name="campaign_detail",
    ),
    path(
        "v1/customers/",
        customer_views.CustomerListView.as_view(),
        name="customer_list_api",
    ),
    path(
        "v1/customer/<customer_uuid>/",
        customer_views.CustomerView.as_view(),
        name="customer_get_api",
    ),
    path(
        "v1/sendingprofiles/",
        sendingprofile_views.SendingProfilesListView.as_view(),
        name="sendingprofile_list_api",
    ),
    path(
        "v1/sendingprofile/<id>/",
        sendingprofile_views.SendingProfileView.as_view(),
        name="sendingprofile_get_api",
    ),
    path(
        "v1/inboundwebhook/",
        webhook_views.IncomingWebhookView.as_view(),
        name="inbound_webhook_api",
    ),
]
