# Generated by Django 4.2.9 on 2024-02-01 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_color_productimage_productvar_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvar',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
