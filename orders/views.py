from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from accounts.permissions import IsArtist, IsKalafexAdmin
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser
from .models import Order, OrderProduct
from .pagination import ResultSetPagination
from .serializers import OrderSerializer, OrderProductSerializer, ParticularOrderSerializer

# Create your views here.

class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'details': serializer.data
            }, status=201)
        else:
            return Response(serializer.errors, status=400)


class OrderModifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def patch(self, request, o_id):
        try:
            obj = Order.objects.get(o_id=o_id)
            serializer = OrderSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'details': serializer.data
                }, status=201)
            else:
                return Response(serializer.errors, status=400)
        except:
            return Response({
                'error': 'Order not found.'
            }, status=404)

    def delete(self, request, o_id):
        try:
            serializer = Order.objects.get(o_id=o_id)
            serializer.delete()
            return Response({
                'status': 'deleted'
            }, status=200)
        except:
            return Response(status=400)


class ParticularOrderView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    parser_classes = [JSONParser]
    lookup_url_kwarg = "o_id"

    def get_queryset(self):
        o_id = self.kwargs.get(self.lookup_url_kwarg)
        order = Order.objects.filter(o_id=o_id)
        return order


class OrderListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = OrderSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        order = Order.objects.filter(user=user)
        return order


class OrderProductCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = OrderProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'details': serializer.data
            }, status=201)
        else:
            return Response(serializer.errors, status=400)


class OrderProductModifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def patch(self, request, op_id):
        try:
            obj = OrderProduct.objects.get(op_id=op_id)
            serializer = OrderProductSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'details': serializer.data
                }, status=201)
            else:
                return Response(serializer.errors, status=400)
        except:
            return Response({
                'error': 'Order not found.'
            }, status=404)

    def delete(self, request, op_id):
        try:
            obj = OrderProduct.objects.get(op_id=op_id)
            obj.delete()
            return Response({
                'status': 'deleted'
            }, status=200)
        except:
            return Response(status=400)


class CartView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = OrderProductSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        order_products = OrderProduct.objects.filter(user=user, ordered=False)
        return order_products
