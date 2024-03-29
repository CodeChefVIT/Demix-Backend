# Generated by Django 3.1.5 on 2021-05-06 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.TextField(null=True)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('display_image', models.ImageField(default='products/image_unavailable.png', upload_to=products.models.product_display_image_path)),
                ('stock_left', models.IntegerField(default=0)),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('demix_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('click_count', models.BigIntegerField(default=0)),
                ('purchase_count', models.BigIntegerField(default=0)),
                ('is_approved', models.BooleanField(default=False)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
            ],
            options={
                'ordering': ['-click_count'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.TextField(null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'verbose_name_plural': 'subcategories',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=products.models.product_image_path)),
                ('mini_description', models.CharField(max_length=255, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.subcategory'),
        ),
    ]
