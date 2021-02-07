from django.shortcuts import render
from .serializers import(
    KalafexAdminRegisterSerializer,
    ArtistRegisterSerializer,
    CustomerRegisterSerializer
)
from .models import(
    User,
    KalafexAdmin,
    Artist,
    Customer
)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

# Create your views here.


class KalafexAdminRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        obj = KalafexAdminRegisterSerializer(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response({
                'status': 'Successfully made user a Kalafex admin.'
            }, status=201)
        else:
            return Response({
                'error': 'Invalid user.'
            }, status=400)


class ArtistRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        obj = ArtistRegisterSerializer(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response({
                'status': 'Successfully made user an artist.'
            }, status=201)
        else:
            return Response({
                'error': 'Invalid user.'
            }, status=400)


class CustomerRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        obj = CustomerRegisterSerializer(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response({
                'status': 'Successfully made user a customer.'
            }, status=201)
        else:
            return Response({
                'error': 'Invalid user.'
            }, status=400)