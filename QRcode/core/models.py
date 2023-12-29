from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    username = models.ForeignKey(
        User, related_name='user', on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    last_edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username)
