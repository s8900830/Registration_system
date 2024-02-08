from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.


class UserProfile(models.Model):
    username = models.ForeignKey(
        User, related_name='user_profiles', on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    last_edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return str(self.username)


class QRCodeList(models.Model):
    username = models.ForeignKey(
        User, related_name='user_qrcodes', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    verify = models.BooleanField(default=False)
    admin_verify = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'QR Code List'
        verbose_name_plural = 'QR Code Lists'

    def __str__(self):
        return str(self.code)
