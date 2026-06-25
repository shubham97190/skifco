from django.urls import path

from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.DonateView.as_view(), name='page'),
    path('success/', views.DonationSuccessView.as_view(), name='success'),
    path('create-order/', views.create_order, name='create-order'),
    path('verify/', views.verify_payment, name='verify'),
]
