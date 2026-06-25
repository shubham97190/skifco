from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='list'),
    path('<slug:slug>/', views.AlbumDetailView.as_view(), name='album'),
]
