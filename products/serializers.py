from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductImage, ReviewRating
from accounts.models import Artist
from accounts.serializers import ArtistSerializer, UserNameIDSerializer
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    class Meta:
        model = Product
        fields = ['pid', 'name', 'artist', 'description', 'category',
                  'subcategory', 'original_price', 'kalafex_price',
                  'display_image', 'discount_price', 'stock_left']
        read_only_fields = ['kalafex_price']

    def create(self, validated_data):
        return Product.objects.create(**validated_data)


class ParticularProductSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField('_get_related_images')
    artist = serializers.SerializerMethodField('_get_related_artist')

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

    def _get_related_artist(self, obj):
        try:
            required_artist = Artist.objects.get(user=obj.artist)
            serialized_artist = ArtistSerializer(required_artist, 
                                             context=self.context).data
            return serialized_artist
        except:
            return None

    class Meta:
        model = Product
        fields = ['pid', 'name', 'description', 'category', 'subcategory', 
                  'stock_left', 'kalafex_price', 'artist', 'original_price',
                  'discount_price', 'display_image', 'image_list']


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('_get_image_url')

    def _get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

    class Meta:
        model = ProductImage
        fields = ['product', 'image', 'mini_description']


class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductWithArtistSerializer(serializers.ModelSerializer):
    artist = serializers.SerializerMethodField('_get_artist_details')

    def _get_artist_details(self, obj):
        artist = User.objects.get(id=obj.artist.id)
        serializer = UserSerializer(artist)
        return serializer.data

    class Meta:
        model = Product
        fields = ['pid', 'name', 'artist', 'description', 'category', 'subcategory', 
                  'stock_left', 'kalafex_price', 'original_price',
                  'discount_price', 'display_image']


class ReviewRatingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('_get_user_details')

    def _get_user_details(self, obj):
        user = User.objects.get(id=obj.user.id)
        serializer = UserNameIDSerializer(user)
        return serializer.data

    class Meta:
        model = ReviewRating
        fields = '__all__'


class ReviewRatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRating
        fields = '__all__'