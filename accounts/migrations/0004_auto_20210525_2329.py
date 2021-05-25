# Generated by Django 3.1.5 on 2021-05-25 17:59

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_artist_cover_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='cover_picture',
            field=models.ImageField(default='uploads/cover_pictures/default.jpg', null=True, upload_to=accounts.models.cover_image_directory_path, verbose_name='cover picture'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='profile_picture',
            field=models.ImageField(default='uploads/profile_pictures/default.jpg', null=True, upload_to=accounts.models.image_directory_path, verbose_name='profile picture'),
        ),
    ]
