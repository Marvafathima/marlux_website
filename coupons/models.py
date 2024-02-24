from django.db import models

# Create your models here.
from django.utils import timezone
from category .models import Products,Category
from home .models import CustomUser
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    expiration_date = models.DateTimeField()
    usage_limit = models.IntegerField(default=1)
    usage_count = models.IntegerField(default=0)
    purchase_count=models.IntegerField(default=0)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    active = models.BooleanField(default=True)
    user_limit = models.IntegerField(default=1)
    user_count=models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def is_valid(self):
        return self.active and self.usage_count < self.usage_limit  and self.user_count < self.user_limit  and self.expiration_date > timezone.now()

    def save(self, *args, **kwargs):
        # Convert your_field to uppercase before saving
        self.code = self.code.upper()
        super(Coupon, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.code