from django.contrib import admin
from django.urls import path, include

from reports.views import HomePageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/', include('reports.urls')),
    path('tasks/', include('tasks.urls')),
    path("", HomePageView.as_view()),
]
