from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin
import uuid
import os
# Create your models here.

def image_directory_path(instance, filename):
    ext = filename.split('.')[1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join('uploads/profile_pictures/', filename)

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.TextField()
    phone_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    #Public types
    is_customer = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)

    #Kalafex administration
    is_kalafex_admin = models.BooleanField(default=False)

    #Website administration
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    #REQUIRED_FIELDS = ['full_name', 'is_kalafex_admin', 'is_artist', 
    #                   'is_customer']


class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    profile_picture = models.ImageField(verbose_name='profile picture',
                                        upload_to=image_directory_path,
                                        default='uploads/profile_pictures/default.png',
                                        null=True)


class KalafexAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    date_of_birth = models.DateField() #YYYY-MM-DD
    address = models.TextField()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    date_of_birth = models.DateField() #YYYY-MM-DD
    address = models.TextField()
