from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('user_info/', views.user_info, name="user_info"),
    path('edit_info/', views.edit_info, name="edit_info"),
    path('<str:url_suffix>/', views.your_view_function),
]
