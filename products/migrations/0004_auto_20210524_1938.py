# Generated by Django 3.1.5 on 2021-05-24 14:08

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210523_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=products.models.product_image_path),
        ),
    ]
