# Generated by Django 4.2.9 on 2024-03-05 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_mamngmnt', '0013_order_payment_mode_order_tracking_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]