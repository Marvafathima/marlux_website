
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from category .models import ProductVar
from .managers import CustomUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserAddress(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE ,related_name='useraddress')
    user_name=models.CharField(max_length=100,default='nil')
    phone_number=models.CharField(max_length=15,default='nil')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    landmark = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_qnty=models.PositiveIntegerField(default=1,null=True)
    total_price=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True)        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVar, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    item_total_price=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True) 
    def save(self, *args, **kwargs):
        self.item_total_price = self.quantity * self.product_variant.price
        super().save(*args, **kwargs)


# import uuid
# from django.utils import timezone 


# class User(models.Model):
#     email = models.EmailField(max_length=254, unique=True)
#     user_name = models.CharField(max_length=254, null=True, blank=True)
#     phone_number=models.CharField(max_length=15)
#     password=models.CharField(max_length=15)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     last_login = models.DateTimeField(null=True, blank=True)
#     date_joined = models.DateTimeField(auto_now_add=True)


# class Profile(models.Model):
#     user=models.OneToOneField(User,   on_delete=models.CASCADE,related_name="profile")
#     phone_number=models.CharField(max_length=15)
#     otp=models.CharField(max_length=100,null=True,blank=True)
#     uid=models.CharField(default=f'{uuid.uuid4}',max_length=200)