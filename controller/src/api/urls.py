"""
API URLs.

This lists all urls under the API app.
"""
# Third-Party Libraries
from api.views import subscription_views
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
]
