# Generated by Django 4.2.9 on 2024-02-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_mamngmnt', '0002_remove_order_order_name_remove_orderproduct_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True),
        ),
    ]
