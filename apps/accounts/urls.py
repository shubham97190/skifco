from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('donations/', views.DonorHistoryView.as_view(), name='donor-history'),
    path('applications/', views.MyApplicationsView.as_view(), name='my-applications'),
    path('applications/<str:ref>/', views.ApplicationStatusView.as_view(), name='application-status'),
]
