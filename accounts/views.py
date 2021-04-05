from django.shortcuts import render
from .models import(
    User,
    KalafexAdmin,
    Artist,
    Customer,
    Address
)
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import (
    KalafexAdminSerializer,
    ArtistCreateSerializer,
    ArtistSerializer,
    CustomerSerializer,
    AddressSerialzier
)
from .pagination import ResultSetPagination
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.


class KalafexAdminRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        obj = KalafexAdminSerializer(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response({
                'status': 'success',
                'details': obj.data
            }, status=201)
        else:
            return Response(obj.errors, status=400)


class ArtistRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request):
        #request.data['user'] = request.user.id
        obj = ArtistCreateSerializer(data=request.data, context={'request': request})
        if obj.is_valid():
            obj.save()
            return Response({
                'status': 'success',
                'details': obj.data
            }, status=201)
        else:
            return Response(obj.errors, status=400)


class CustomerRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        obj = CustomerCreateSerializer(data=request.data, context={'request': request})
        if obj.is_valid():
            obj.save()
            return Response({
                'status': 'success',
                'details': obj.data
            }, status=201)
        else:
            return Response(obj.errors, status=400)


class AddressCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        obj = AddressSerialzier(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response({
                'status': 'success',
                'details': obj.data
            }, status=201)
        else:
            return Response(obj.errors, status=400)


class ArtistUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    serializer_class = ArtistSerializer

    def get_object(self):
        user = self.request.user
        artist = Artist.objects.get(user=user)
        return artist


class CustomerUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    serializer_class = CustomerSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        return customer


class ParticularAddressView(ListAPIView):
    parser_classes = [JSONParser]
    serializer_class = AddressSerialzier
    lookup_url_kwarg = 'a_id'

    def get_queryset(self):
        a_id = self.kwargs.get(self.lookup_url_kwarg)
        address = Address.objects.filter(a_id=a_id)
        return address


class AddressListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = AddressSerialzier

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        address = Address.objects.filter(user=user)
        return address

class AddressUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = AddressSerialzier
    lookup_field = 'a_id'

    def get_queryset(self, *args, **kwargs):
        a_id = self.kwargs.get(self.lookup_field)
        address = Address.objects.filter(a_id=a_id)
        return address


class ParticularArtistView(ListAPIView):
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    serializer_class = ArtistSerializer
    lookup_url_kwarg = 'custom_url'

    def get_queryset(self):
        custom_url = self.kwargs.get(self.lookup_url_kwarg)
        artist = Artist.objects.filter(custom_url=custom_url)
        return artist


class ArtistListView(ListAPIView):
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    serializer_class = ArtistSerializer
    pagination_class = ResultSetPagination
    queryset = Artist.objects.all()