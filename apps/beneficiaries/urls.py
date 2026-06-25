from django.urls import path

from . import views

app_name = 'beneficiaries'

urlpatterns = [
    path('', views.ApplicationCreateView.as_view(), name='apply'),
]
