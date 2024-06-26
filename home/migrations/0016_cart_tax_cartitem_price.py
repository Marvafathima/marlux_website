# Generated by Django 4.2.9 on 2024-02-20 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_cart_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
