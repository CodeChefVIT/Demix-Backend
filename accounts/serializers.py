from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import KalafexAdmin, Artist, Customer

User = get_user_model()


class KalafexAdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KalafexAdmin
        fields = '__all__'



class ArtistRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'



class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'