# Generated by Django 4.2.9 on 2024-02-20 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_cart_tax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='tax',
        ),
    ]
