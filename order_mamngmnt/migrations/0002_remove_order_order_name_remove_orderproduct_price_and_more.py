# Generated by Django 4.2.9 on 2024-02-17 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_mamngmnt', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_name',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='price',
        ),
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
