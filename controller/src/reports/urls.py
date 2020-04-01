from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
  path('', views.reports_page, name='reports-page'),
  path('pdf', views.generate_pdf, name='generate_pdf'),
]
