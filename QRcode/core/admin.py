from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import UserProfile, QRCodeList

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(QRCodeList)
