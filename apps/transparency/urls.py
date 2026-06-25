from django.urls import path

from . import views

app_name = 'transparency'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='list'),
]
