# Generated by Django 4.2.9 on 2024-02-19 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_cart_cart_total_cart_shipping'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
