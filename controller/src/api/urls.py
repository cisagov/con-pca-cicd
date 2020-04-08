from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
     path("v1/subscriptions/", views.SubscriptionsView.as_view(), name="subscriptions_api")
]
