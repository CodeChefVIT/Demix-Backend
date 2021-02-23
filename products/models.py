from django.db import models
from accounts.models import Artist
from django.contrib.auth import get_user_model
import uuid

# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'subcategories'


def product_display_image_path(instance, filename):
    return f"products/{instance.pid}/{filename}/"

def product_image_path(instance, filename):
    return f"products/{instance.product.pid}/{filename}/"

class Product(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.TextField()
    description = models.TextField()
    display_image = models.ImageField(
        upload_to=product_display_image_path,
        default='products/image_unavailable.png'
    )
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    stock_left = models.IntegerField(default=0)
    price = models.CharField(max_length=255)
    click_count = models.BigIntegerField(default=0)
    purchase_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-click_count']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_path)
    mini_description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.id}"
