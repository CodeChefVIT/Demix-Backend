from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import KalafexAdmin, Artist, Customer, Address

User = get_user_model()


class KalafexAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = KalafexAdmin
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class AddressSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'