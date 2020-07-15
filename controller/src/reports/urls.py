# Third-Party Libraries
from django.conf.urls import url
from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "<subscription_uuid>/monthly/<start_date>/",
        views.MonthlyReportsView.as_view(),
        name="monthly-reports-page",
    ),
    path(
        "<subscription_uuid>/cycle/<start_date>/",
        views.CycleReportsView.as_view(),
        name="cycle-reports-page",
    ),
    path(
        "<subscription_uuid>/yearly/<start_date>/",
        views.YearlyReportsView.as_view(),
        name="yearly-reports-page",
    )  
]
