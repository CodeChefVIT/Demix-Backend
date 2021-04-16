from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import KalafexAdmin, Artist, Customer, Address
from djoser.serializers import UserSerializer

User = get_user_model()


class KalafexAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = KalafexAdmin
        fields = '__all__'


class ArtistCreateSerializer(serializers.ModelSerializer):
    # See https://stackoverflow.com/questions/52367379/why-is-django-rest-frameworks-request-data-sometimes-immutable
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    class Meta:
        model = Artist
        fields = '__all__'
        read_only_fields = ['balance', 'cashout_requested']

class ArtistSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField('_get_image_url')
    
    def _get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.profile_picture.url)

    class Meta:
        model = Artist
        fields = ['user', 'bio', 'custom_url', 'profile_picture']


class ArtistModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'
        read_only_fields = ['balance', 'cashout_requested']


class ArtistPersonalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_views = serializers.SerializerMethodField('_get_artist_product_hits')
    total_sales = serializers.SerializerMethodField('_get_artist_sales')
    total_earnings = serializers.SerializerMethodField('_get_artist_earnings')
    total_orders = serializers.SerializerMethodField('_get_artist_order_count')

    def _get_artist_product_hits(self, obj):
        hits = obj.get_cumulative_product_hits
        return hits

    def _get_artist_sales(self, obj):
        sales = obj.get_cumulative_sales
        return sales

    def _get_artist_earnings(self, obj):
        earnings = obj.get_cumulative_earnings
        return earnings

    def _get_artist_order_count(self, obj):
        order_count = obj.get_cumulative_order_count
        return order_count
    
    class Meta:
        model = Artist
        fields = '__all__'
        read_only_fields = ['balance', 'cashout_requested']


class CustomerCreateSerializer(serializers.ModelSerializer):
    # See https://stackoverflow.com/questions/52367379/why-is-django-rest-frameworks-request-data-sometimes-immutable
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField('_get_image_url')
    
    def _get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.profile_picture.url)

    class Meta:
        model = Customer
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'