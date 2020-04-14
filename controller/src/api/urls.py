"""
API URLs.

This lists all urls under the API app.
"""
# Third-Party Libraries
from api.views import subscription_views, target_views, template_views
from django.urls import path

urlpatterns = [
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
    path("v1/targets/", target_views.TargetListView.as_view(), name="target_list_api",),
    path(
        "v1/targets/<target_uuid>/",
        target_views.TargetView.as_view(),
        name="target_get_api",
    ),
]
