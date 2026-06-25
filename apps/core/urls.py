from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.PageDetailView.as_view(), name='about', kwargs={'slug': 'about'}),
    path('objectives/', views.PageDetailView.as_view(), name='objectives', kwargs={'slug': 'objectives'}),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy-policy/', views.PageDetailView.as_view(), name='privacy-policy', kwargs={'slug': 'privacy-policy'}),
    path('terms/', views.PageDetailView.as_view(), name='terms', kwargs={'slug': 'terms'}),
    path('refund-policy/', views.PageDetailView.as_view(), name='refund-policy', kwargs={'slug': 'refund-policy'}),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter-subscribe'),
]
