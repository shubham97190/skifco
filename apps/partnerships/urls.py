from django.urls import path

from . import views

app_name = 'partnerships'

urlpatterns = [
    path('', views.CSRPartnershipsView.as_view(), name='page'),
    path('enquire/', views.CSRInquiryCreateView.as_view(), name='enquire'),
]
