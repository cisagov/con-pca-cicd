# Third-Party Libraries
from django.conf.urls import url
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="run_task"),
    path("<task_id>/", views.TaskView.as_view(), name="get_status"),
]
