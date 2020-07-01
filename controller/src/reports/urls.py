# Third-Party Libraries
from django.conf.urls import url
from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "<subscription_uuid>/monthly/",
        views.MonthlyReportsView.as_view(),
        name="monthly-reports-page",
    ),
    path(
        "<subscription_uuid>/cycle/",
        views.CycleReportsView.as_view(),
        name="cycle-reports-page",
    ),
    path(
        "<subscription_uuid>/yearly/",
        views.YearlyReportsView.as_view(),
        name="yearly-reports-page",
    )  
]
