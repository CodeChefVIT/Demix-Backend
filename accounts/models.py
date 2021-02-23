from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin
import uuid
import os
from django.utils.translation import ugettext_lazy as _

# Create your models here.

def image_directory_path(instance, filename):
    ext = filename.split('.')[1]
    filename = f"{instance._id}.{ext}"

    return f"users/profile_pictures/{filename}"

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

    def __str__(self):
        return self.full_name

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name', 'is_kalafex_admin', 'is_artist', 
                       'is_customer']


class KalafexAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)

    def __str__(self):
        return self.user.full_name


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    date_of_birth = models.DateField() #YYYY-MM-DD
    profile_picture = models.ImageField(verbose_name='profile picture',
                                        upload_to=image_directory_path,
                                        default='uploads/profile_pictures/default.png',
                                        null=True)
    
    def __str__(self):
        return self.user.full_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    date_of_birth = models.DateField() #YYYY-MM-DD
    profile_picture = models.ImageField(verbose_name='profile picture',
                                        upload_to=image_directory_path,
                                        default='uploads/profile_pictures/default.png',
                                        null=True)

    def __str__(self):
        return self.user.full_name


ADDRESS_CHOICES = (
    ('Billing', _('Billing')),
    ('Shipping', _('Shipping'))
)

class BillingAddress(models.Model):
    ba_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.TextField()
    apartment_address = models.TextField()
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=8, choices=ADDRESS_CHOICES)
    
    def __str__(self):
        return f"{self.user.full_name}'s {self.address_type} address"