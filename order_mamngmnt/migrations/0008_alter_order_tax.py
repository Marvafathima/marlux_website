# Generated by Django 4.2.9 on 2024-02-20 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_mamngmnt', '0007_alter_order_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.FloatField(null=True),
        ),
    ]
