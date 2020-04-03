from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscribe, name='subscribe'),
    path('dhl/', views.dhl_view, name='dhl'),
    path('view_campaigns', views.view_campaigns, name='view-campaigns')
]
