# Generated by Django 4.2.9 on 2024-02-25 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0004_alter_coupon_purchase_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='purchase_count',
            field=models.IntegerField(null=True),
        ),
    ]
