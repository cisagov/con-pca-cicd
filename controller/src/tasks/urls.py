from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
  path('', views.run_task, name='run_task'),
  path("tasks/<task_id>/", views.get_status, name="get_status"),
]
