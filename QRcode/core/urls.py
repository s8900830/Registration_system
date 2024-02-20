from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('account/login/', views.home, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
    path('user_info/', views.user_info, name="user_info"),
    path('edit_info/', views.edit_info, name="edit_info"),
    path('manage/', views.group, name="manage"),
    path('manage/<int:pk>/<str:action>', views.group_list, name="manage"),
    path('change_permission/<int:pk>', views.change_permission, name="change_permission"),
    path('admin_user_edit/<int:pk>', views.admin_user_edit, name="admin_user_edit"),
    path('generate_qr_code/', views.QRcode, name="generate_qr_code"),
    path('admin_user_pas_change/<int:pk>',views.admin_user_pas_change , name="admin_user_pas_change"),
    path('<str:url_suffix>/', views.verify), #要注意一下 可能會有問題
]
