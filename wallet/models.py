from django.db import models
from home .models import CustomUser
# Create your models here.
class Wallet(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_wallet")
    balance=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Refund', 'Refund'),
        ('Purchase', 'Purchase'),
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)