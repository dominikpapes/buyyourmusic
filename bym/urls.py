from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('albums/<int:id>/', views.album_detail, name="album_detail")
]