from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('account/login/', views.home, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('user_info/', views.user_info, name="user_info"),
    path('edit_info/', views.edit_info, name="edit_info"),
    path('manage/', views.group_list, name="manage"),
    path('manageuser/', views.manageuser, name="manageuser"),
    path('change_permission/', views.change_permission, name="change_permission"),
    path('generate_qr_code/', views.QRcode, name="generate_qr_code"),
    path('<str:url_suffix>/', views.verify),
]
