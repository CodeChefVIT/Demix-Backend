from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from accounts.permissions import IsArtist, IsKalafexAdmin
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser
from .models import Order, OrderProduct, Payment, Refund
from .pagination import ResultSetPagination
from .serializers import(
    OrderSerializer,
    OrderProductSerializer,
    OrderProductCrudSerializer,
    ParticularOrderSerializer,
    PaymentSerializer,
    RefundOrderSerializer,
    RefundSerializer
)
from accounts.permissions import IsKalafexAdmin

import razorpay

# Create your views here.

client = razorpay.Client(auth=("rzp_test_lVBKYGGW6umcct", "syQEJEUbw0vZyTnKfZ8ApVqJ"))


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


class PreviousOrdersListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = OrderSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        order = Order.objects.filter(user=user,
                                     payment__paid_successfully=True)
        return order


class OrderProductCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = OrderProductCrudSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'details': serializer.data
                }, status=201)
            else:
                return Response(serializer.errors, status=400)
        except: # IntegrityError
            return Response({
                'status': 'error',
                'details': 'Invalid pid.'
            }, status=400)


class OrderProductModifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def patch(self, request, op_id):
        try:
            obj = OrderProduct.objects.get(op_id=op_id)
            serializer = OrderProductCrudSerializer(obj, data=request.data, 
                                                    partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'details': serializer.data
                }, status=201)
            else:
                return Response(serializer.errors, status=400)
        except OrderProduct.DoesNotExist:
            return Response({
                'error': 'OrderProduct not found.'
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


class PaymentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        try:
            obj = Payment.objects.get(order=request.data['order'])
            if obj.paid_successfully:
                return Response({
                    'status': 'error',
                    'details': 'Order already paid for.'
                }, status=400)
            serializer = PaymentSerializer(obj)
            razorpay_details = client.order.fetch(obj.razorpay_order_id)
            return Response({
                'status': 'success',
                'razorpay_details': razorpay_details,
                'internal_details': serializer.data
            }, status=200)
        except (Payment.DoesNotExist, KeyError):
            try:
                request.data['user'] = request.user.id
                order = Order.objects.get(o_id=request.data['order'])
                #Convert to paise
                amount = float(order.get_total) * 100
                request.data['amount'] = float(order.get_total)
                data = {
                    'amount': amount,
                    'currency': 'INR',
                    'receipt': request.data['order'],
                    'notes': {
                        'user_id': request.user.id,
                        'name': request.user.full_name,
                        'internal_order_id': request.data['order']
                    }
                }
                razorpay_order = client.order.create(data=data)
                request.data['razorpay_order_id'] = razorpay_order['id']
                payment_object = PaymentSerializer(data=request.data)
                if payment_object.is_valid():
                    payment_object.save()
                    return Response({
                        'status': 'success',
                        'razorpay_details': razorpay_order,
                        'internal_details': payment_object.data
                    }, status=201)
                else:
                    return Response(payment_object.errors, status=400)
            except (Order.DoesNotExist, KeyError):
                return Response({
                    'status': 'error',
                    'details': 'Error creating payment.'
                }, status=400)
            except Exception as e:
                return Response({
                    'status': 'error',
                    'details': str(e)
                }, status=400)


class PaymentVerifyView(APIView):
    # We don't use parsers for the Razorpay webhook. The data is meant to be processed raw,
    # without any parsing or so in the middle.

    def get(self, request):
        if request.data['razorpay_payment_id']:
            try:
                webhook_signature = request.headers.get('X-Razorpay-Signature')
                result = client.utility.verify_webhook_signature(request.data, # pass raw data
                                                                 webhook_signature,
                                                                 webhook_secret) #set secret up
                obj = Payment.objects.get(razorpay_order_id=request.data['razorpay_order_id'])
                obj.paid_successfully = True
                obj.save()
                order = Order.objects.get(o_id=obj.order)
                for order_product in order.order_products.all():
                    order_product.product.purchase_count += order_product.quantity
                    order_product.artist.balance += (
                        order_product.quantity * order_product.product.original_price
                    )
                    order_product.save()
            except:
                pass


class RequestRefundView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    
    def post(self, request):
        order_id = request.data['order']
        try:
            obj = Order.objects.get(o_id=order_id)
            if obj.payment.paid_successfully:
                # --!--
                request.data['accepted'] = False
                refund_serializer = RefundSerializer(data=request.data)
                if refund_serializer.is_valid():
                    refund_serializer.save()
                    obj.refund_requested = True
                    obj.save()
                    serializer = OrderSerializer(obj)
                    return Response({
                        'status': 'success',
                        'order_details': serializer.data,
                        'refund_details': refund_serializer.data
                    }, status=200)
                else:
                    return Response({
                        'status': 'error',
                        'detail': 'Error creating a refund object.'
                    }, status=400)
            else:    
                return Response({
                    'status': 'error',
                    'details': 'Order has not been paid for.'
                }, status=400)
        except Order.DoesNotExist:
            return Response({
                'status': 'error',
                'details': 'Order not found.'
            }, status=400)


class RefundRequestsView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsKalafexAdmin]
    parser_classes = [JSONParser]
    serializer_class = RefundOrderSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self, *args, **kwargs):
        refund_orders = Order.objects.filter(refund_requested=True,
                                      refund_granted=False)
        return refund_orders


class GrantRefundView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsKalafexAdmin]
    parser_classes = [JSONParser]
    serializer_class = RefundOrderSerializer

    def post(self, request):
        try:
            order = Order.objects.get(o_id=request.data['order'])
            refund = Refund.objects.get(order=order.o_id)
            order.refund_granted = True
            order.save()
            refund.accepted = True
            refund.save()
            return Response({
                'status': 'success',
                'details': 'Stored successful refund grant.'
            }, status=200)
        except:
            return Response({
                'status': 'error',
                'detail': 'Refund has not been requested for this order.'
            }, status=400)