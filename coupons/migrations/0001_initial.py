# Generated by Django 4.2.9 on 2024-02-22 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0007_alter_productvar_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('expiration_date', models.DateTimeField()),
                ('usage_limit', models.IntegerField(default=1)),
                ('usage_count', models.IntegerField(default=0)),
                ('minimum_order_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('active', models.BooleanField(default=True)),
                ('user_limit', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('applicable_categories', models.ManyToManyField(blank=True, to='category.category')),
                ('applicable_products', models.ManyToManyField(blank=True, to='category.products')),
            ],
        ),
    ]
