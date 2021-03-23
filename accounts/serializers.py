from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import KalafexAdmin, Artist, Customer, Address

User = get_user_model()


class KalafexAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = KalafexAdmin
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField('_get_image_url')
    
    def _get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.profile_picture.url)

    class Meta:
        model = Artist
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField('_get_image_url')
    
    def _get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.profile_picture.url)

    class Meta:
        model = Customer
        fields = '__all__'

class AddressSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'