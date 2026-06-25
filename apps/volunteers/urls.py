from django.urls import path

from . import views

app_name = 'volunteers'

urlpatterns = [
    path('', views.VolunteerSignupView.as_view(), name='signup'),
]
