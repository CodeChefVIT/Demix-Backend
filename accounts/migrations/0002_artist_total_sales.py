# Generated by Django 3.1.5 on 2021-05-11 08:21

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='total_sales',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14),
        ),
    ]