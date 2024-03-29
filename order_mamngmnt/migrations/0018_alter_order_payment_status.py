# Generated by Django 4.2.9 on 2024-03-09 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_mamngmnt', '0017_alter_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('cod', 'COD'), ('wallet', 'Wallet'), ('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=10),
        ),
    ]
