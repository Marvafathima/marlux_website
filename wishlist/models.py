from django.db import models
from home .models import CustomUser,UserAddress
from category.models import ProductImage,Products,ProductVar

# Create your models here.
class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models. CASCADE,related_name="user_wishlist")
    product=models.ForeignKey(Products,on_delete=models. CASCADE,related_name="wishlist_product")
    created_at=models.DateField(auto_now_add=True)

