from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('albums/<int:id>/', views.album_detail, name="album_detail"),
    path('bym_admin/', views.admin_home, name='admin_home'),
    path('bym_adim/albums/new/', views.album_create, name='album_create'),
    path('bym_adim/albums/<int:id>/edit/', views.album_edit, name='album_edit'),
    path('bym_adim/albums/<int:id>/delete/', views.album_delete, name='album_delete'),
]