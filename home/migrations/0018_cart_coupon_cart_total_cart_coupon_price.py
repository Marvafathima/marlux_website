# Generated by Django 4.2.9 on 2024-02-24 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_cart_coupon_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon_cart_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
