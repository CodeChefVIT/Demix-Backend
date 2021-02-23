from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pid','display_image', 'name', 'price', 'artist', 'category', 'subcategory']


class ParticularProductSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField('_get_related_images')

    def _get_related_images(self, obj):
        images = ProductImage.objects.filter(
            product=obj.pid
        )
        image_list = ProductImageSerializer(
            images, 
            many=True,
            context=self.context
        ).data
        return image_list

    class Meta:
        model = Product
        fields = ['pid', 'name', 'description', 'category', 'subcategory', 
                  'stock_left', 'price', 'artist', 'display_image', 'image_list']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('_get_image_url')

    def _get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

    class Meta:
        model = ProductImage
        fields = ['image', 'mini_description']