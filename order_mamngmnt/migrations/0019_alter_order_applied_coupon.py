# Generated by Django 4.2.9 on 2024-03-09 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0006_alter_coupon_purchase_count'),
        ('order_mamngmnt', '0018_alter_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='applied_coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_coupon', to='coupons.coupon'),
        ),
    ]
