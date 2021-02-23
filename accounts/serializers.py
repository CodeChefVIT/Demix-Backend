from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import KalafexAdmin, Artist, Customer
from djoser.serializers import UserCreateSerializer

User = get_user_model()
