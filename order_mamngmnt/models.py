from django.db import models
from home .models import CustomUser,CartItem,Cart,Address,UserAddress
from category .models import Products,ProductVar,ProductImage
from decimal import Decimal


# Create your models here.
# class Payment(models.Model):
#     user=models.ForeignKey(Account, on_delete=models.CASCADE)
#     Payment_id=models.CharField(max_length=100)
#     payment_method=models.CharField(max_length=100)
#     created_at=models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.Payment_id

class OrderAddress(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE ,related_name='orderaddress')
    house_name=models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    landmark = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country= models.CharField(max_length=100)


class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Delivered','Delevered'),
        ('Cancelled','Cancelled'),
        ('Return','Return')

    )
    PAYMENT_STATUS_CHOICES = (
        ('cod', 'COD'),
        ('wallet',"Wallet"),
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('refunded','Refunded')
    )
    user=models.ForeignKey(CustomUser, on_delete=models. CASCADE,related_name="user_order")
    address=models.ForeignKey(OrderAddress, on_delete=models.CASCADE,null=True,related_name="address_order")
    order_total=models.FloatField(null=True) 
    discount_total=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True)
    discount_grand_total=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True)
    applied_coupon=models.IntegerField(null=True)
    tax=models.FloatField(null=True)
    status=models.CharField(max_length=10, choices=STATUS, default='Pending')
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    total_qnty=models.IntegerField(default=1)
    grand_total=models.FloatField(null=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    razorpay_order_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank=True)
    payment_mode=models.CharField(max_length=500,null=True,blank=True)
    tracking_number=models.CharField(max_length=500,null=True,blank=True)
    # coupen=models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate tax as 5% of the order total
        if self.order_total is not None:
            x=0.02
            self.tax = float(x)* float(self.order_total)
            self.grand_total= float(self.order_total) + self.tax
        else:
            self.tax = None
        super().save(*args, **kwargs)




class OrderProduct(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='orderproduct')
    product_variant=models.ForeignKey(ProductVar, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price=models.FloatField(default=0)
    ordered=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    item_total_price=models.DecimalField(default=0,decimal_places=2,max_digits=10,null=True) 
    def save(self, *args, **kwargs):
        self.item_total_price = self.quantity * self.price
        super().save(*args, **kwargs)