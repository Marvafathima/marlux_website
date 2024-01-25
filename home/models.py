from django.db import models
import uuid
from django.utils import timezone 

class User(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    user_name = models.CharField(max_length=254, null=True, blank=True)
    phone_number=models.CharField(max_length=15)
    password=models.CharField(max_length=15)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)


class Profiles(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    phone_number=models.CharField(max_length=15)
    otp=models.CharField(max_length=100,null=True,blank=True)
    uid=models.CharField(default=f'{uuid.uuid4}',max_length=200)