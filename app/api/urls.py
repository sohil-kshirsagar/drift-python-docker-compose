from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health),
    path('weather/', views.weather),
    path('users/<int:user_id>/', views.get_user),
    path('users/', views.create_user),
    path('posts/<int:post_id>/', views.get_post),
    path('posts/', views.create_post),
]
