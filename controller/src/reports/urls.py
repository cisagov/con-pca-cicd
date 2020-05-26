from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    path("<subscription_uuid>/", views.ReportsView.as_view(), name="reports-page"),
    path("pdf", views.generate_pdf, name="generate-pdf"),
]
