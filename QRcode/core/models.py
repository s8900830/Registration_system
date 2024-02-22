from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from functools import partial
import datetime

# Create your models here.


class UserProfile(models.Model):
    username = models.ForeignKey(
        User, related_name='user_profiles', on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    last_edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return str(self.username)
    
    @receiver(post_save, sender=User)
    def update_from_User(sender,instance,created,**kwargs):
        if created :
            UserProfile.objects.create(username=instance,email=instance.email)
        else:
            profile= UserProfile.objects.get(username=instance)
            profile.email = instance.email
            profile.save()

class QRCodeList(models.Model):
    username = models.ForeignKey(
        User, related_name='user_qrcodes', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    verify = models.BooleanField(default=False)
    admin_verify = models.CharField(max_length=20)
    send_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def calculate_expired_at():
        return datetime.date.today() + datetime.timedelta(days=30)

    expired_at = models.DateTimeField(default=calculate_expired_at)

    class Meta:
        verbose_name = 'QR Code List'
        verbose_name_plural = 'QR Code Lists'

    def __str__(self):
        return str(self.code)