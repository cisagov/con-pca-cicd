from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    path("<subscription_uuid>/", views.ReportsView.as_view(), name="reports-page"),
    path("quarter/<subscription_uuid>/<start_date>/", views.CycleReports.as_view(), name="quarterly-reports-page"),
    
]
