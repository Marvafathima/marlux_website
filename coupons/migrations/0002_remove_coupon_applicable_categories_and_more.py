# Generated by Django 4.2.9 on 2024-02-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='applicable_categories',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='applicable_products',
        ),
        migrations.AddField(
            model_name='coupon',
            name='purchase_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='user_limit',
            field=models.IntegerField(default=1),
        ),
    ]
