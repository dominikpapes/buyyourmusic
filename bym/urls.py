from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('albums/<int:id>/', views.album_detail, name="album_detail"),
    path("reviews/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path('bym_admin/', views.admin_home, name='admin_home'),
    path('bym_adim/albums/new/', views.album_create, name='album_create'),
    path('bym_adim/albums/<int:id>/edit/', views.album_edit, name='album_edit'),
    path('bym_adim/albums/<int:id>/delete/', views.album_delete, name='album_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='bym/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
]