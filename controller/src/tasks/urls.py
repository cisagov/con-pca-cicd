from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    path("", views.TaskListView.as_view(), name="run_task"),
    path("<task_id>/", views.TaskView.as_view(), name="get_status"),
]
