from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)