
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from category .models import ProductVar
from coupons .models import Coupon
from .managers import CustomUserManager
from decimal import Decimal,ROUND_HALF_UP


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
    
class Address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE ,related_name='address')
    house_name=models.CharField(max_length=255,default="none")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    landmark = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country= models.CharField(max_length=100,default="none")
    is_default=models.BooleanField(default=False)
class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_qnty=models.PositiveIntegerField(default=1,null=True)
    tax=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True)
    shipping=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True)
    cart_total=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True)
    total_price=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True)        
    is_ordered=models.BooleanField(default=False)
    coupon_count=models.IntegerField(default=0)
    applied_coupon=models.ForeignKey(Coupon,null=True,on_delete=models.CASCADE,related_name="applied_coupon")
    coupon_price=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True)
    coupon_cart_total=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True)
    
    razorpay_order_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank=True)
    
    
    def calculate_cart_total(self):
        self.cart_total = (self.shipping + self.total_price +self.tax).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.coupon_cart_total=(self.shipping + self.coupon_price +self.tax)
    def save(self, *args, **kwargs):
        if self.total_price is not None:
            x=0.02
            self.tax= (Decimal(x) * self.total_price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
        else:
            self.tax = None
        # If total_qnty is zero, set shipping to zero, else set it to 50
        
        if self.total_qnty == 0:
            self.shipping = 0
           
        else:
            self.shipping = 50
        
        # Calculate cart total
        self.calculate_cart_total()

        super().save(*args, **kwargs)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVar, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price=models.DecimalField(default=1,decimal_places=2,max_digits=10,null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    item_total_price=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True) 
    def save(self, *args, **kwargs):
        self.price=self.product_variant.price
        if self.pk:  # If the instance has already been saved (i.e., it's an update)
            old_cart_item = CartItem.objects.get(pk=self.pk)
            if old_cart_item.quantity != self.quantity:  # Check if quantity has changed
                self.item_total_price = self.quantity * self.price
        else:  # If it's a new instance
            self.item_total_price = self.quantity * self.product_variant.price
        
        super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     self.item_total_price = self.quantity * self.product_variant.price
    #     super().save(*args, **kwargs)


