from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('account/login/', views.home, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('user_info/', views.user_info, name="user_info"),
    path('edit_info/', views.edit_info, name="edit_info"),
<<<<<<< HEAD
    path('manage/', views.group_list, name="manage"),
    path('manageuser/', views.manageuser, name="manageuser"),
    path('change_permission/', views.change_permission, name="change_permission"),
    path('generate_qr_code/', views.QRcode, name="generate_qr_code"),
=======
    path('manage/', views.group, name="manage"),
    path('manage/<int:pk>/<str:action>', views.group_list, name="manage"),
    path('change_permission/<int:pk>', views.change_permission, name="change_permission"),
    path('admin_user_edit/<int:pk>', views.admin_user_edit, name="admin_user_edit"),
    # path('generate_qr_code/', views.QRcode, name="generate_qr_code"),
>>>>>>> 23daefd48e43e22c61ce5e5f994f4cc94344bf60
    path('<str:url_suffix>/', views.verify),
]
