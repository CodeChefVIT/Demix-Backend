from decimal import Decimal

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
from .permissions import IsKalafexAdmin, IsArtist
from rest_framework.views import APIView
from .serializers import (
    KalafexAdminSerializer,
    ArtistCreateSerializer,
    ArtistSerializer,
    ArtistModifySerializer,
    ArtistPersonalSerializer,
    CustomerSerializer,
    AddressSerializer
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
        try:
            obj = ArtistCreateSerializer(data=request.data, context={'request': request})
            if obj.is_valid():
                obj.save()
                return Response({
                    'status': 'success',
                    'details': obj.data
                }, status=201)
        except Artist.DoesNotExist:
            return Response({
                'status': 'error',
                'details': 'This user already has an Artist profile.'
            }, status=400)
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
        obj = AddressSerializer(data=request.data)
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
    serializer_class = ArtistModifySerializer

    def get_object(self):
        user = self.request.user
        artist = Artist.objects.get(user=user)
        return artist


class ArtistPersonalInsightsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsArtist]
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def get(self, request):
        user = request.user.id
        try:
            artist_profile = Artist.objects.get(user=user)
            serializer = ArtistPersonalSerializer(artist_profile)
            return Response({
                'status': 'success',
                'details': serializer.data
            }, status=200)
        except Artist.DoesNotExist:
            return Response({
                'status': 'error',
                'details': 'Artist profile does not exist for this user.'
            }, status=400)
        except:
            return Response({
                'status': 'error',
                'details': 'Error registering an Artist profile.'
            }, status=400)


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
    serializer_class = AddressSerializer
    lookup_url_kwarg = 'a_id'

    def get_queryset(self):
        a_id = self.kwargs.get(self.lookup_url_kwarg)
        address = Address.objects.filter(a_id=a_id)
        return address


class AddressListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = AddressSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        address = Address.objects.filter(user=user)
        return address

class AddressUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = AddressSerializer
    lookup_field = 'a_id'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        a_id = self.kwargs.get(self.lookup_field)
        address = Address.objects.filter(user=user, a_id=a_id)
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

class CashOutRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsArtist]
    parser_classes = [JSONParser]

    def post(self, request):
        user = request.user.id
        try:
            artist = Artist.objects.get(user=user)
            if artist.cashout_requested:
                return Response({
                    'status': 'success',
                    'details': 'Already requested cash-out.'
                }, status=200)
            else:
                artist.cashout_requested = True
                artist.save()
                return Response({
                    'status': 'success',
                    'details': 'Successfully requested cash-out.'
                }, status=201)
        except:
            return Response({
                'status': 'error',
                'details': 'Artist error.'
            }, status=400)


class CashOutView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsKalafexAdmin]
    parser_classes = [JSONParser]
    serializer_class = ArtistPersonalSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self, *args, **kwargs):
        requested_artists = Artist.objects.filter(cashout_requested=True)
        return requested_artists


class GrantCashOutView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsKalafexAdmin]
    parser_classes = [JSONParser]
    
    def post(self, request):
        try:
            artist = Artist.objects.get(user=request.data['user'])
            artist.cashout_requested = False
            artist.balance = Decimal('0.00')
            artist.save()
            return Response({
                'status': 'success',
                'details': 'Cash-out granted.'
            }, status=201)
        except Artist.DoesNotExist:
            return Response({
                'status': 'error',
                'details': 'Artist does not exist.'
            }, status=400)