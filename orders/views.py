from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from accounts.permissions import IsArtist, IsDemixAdmin, IsArtist
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import JSONParser
from rest_pandas import PandasView, PandasExcelRenderer
from .models import Order, OrderProduct, Payment, Refund
from .pagination import ResultSetPagination
from .serializers import(
    OrderSerializer,
    OrderProductSerializer,
    OrderProductCrudSerializer,
    OrderProductExportSerializer,
    PaymentSerializer,
    RefundOrderSerializer,
    RefundSerializer,
    OrderDeliverySerializer,
    OrderProductHandOverSerializer
)
from accounts.permissions import IsDemixAdmin
from accounts.models import Address, Artist
from products.models import Product

import razorpay
import json
import datetime
from django.utils.timezone import make_aware, now

# Create your views here.

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))


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
            user = request.user.id
            obj = Order.objects.get(o_id=o_id, user=user)
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
            user = request.user.id
            serializer = Order.objects.get(o_id=o_id, user=user)
            serializer.delete()
            return Response({
                'status': 'deleted'
            }, status=200)
        except:
            return Response({
                'error': 'Order not found.'
            }, status=404)


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


class CurrentAndPreviousOrdersListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]
    serializer_class = OrderSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        order = Order.objects.filter(
            user=user,
            payment__paid_successfully=True).order_by('-start_date')
        return order


class OrderProductCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request):
        request.data['user'] = request.user.id
        user = request.data['user']
        try:
            pid = request.data['product']
            if OrderProduct.objects.filter(product=pid, ordered=False, user=user).exists():
                return Response({
                    'status': 'error',
                    'details': 'Product already added to cart.'
                }, status=400)
            product = Product.objects.get(pid=pid)
            if product.stock_left < int(request.data['quantity']):
                return Response({
                    'status': 'error',
                    'details': 'Not enough stock.'
                }, status=400)
            serializer = OrderProductCrudSerializer(data=request.data)
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
            user = request.user.id
            obj = OrderProduct.objects.get(op_id=op_id, user=user)

            if 'order' in request.data.keys():
                if not Order.objects.filter(user=user, o_id=request.data['order']).exists():
                    return Response({
                        'status': 'error',
                        'details': 'Unauthorized to add to the given order.'
                    }, status=400)
                    
            if 'quantity' in request.data.keys():
                product = Product.objects.get(pid=obj.product.pid)
                if product.stock_left < int(request.data['quantity']):
                    return Response({
                        'status': 'error',
                        'details': 'Not enough stock.'
                    }, status=400)
            
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
        except ValidationError:
            return Response({
                'error': 'Enter valid ID.'
            }, status=404)

    def delete(self, request, op_id):
        try:
            user = request.user.id
            obj = OrderProduct.objects.get(op_id=op_id, user=user)
            obj.delete()
            return Response({
                'status': 'deleted'
            }, status=200)
        except:
            return Response({
                'status': 'error',
                'details': 'Unauthorized.'
            }, status=400)


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
                        'email': request.user.email,
                        'phone_number': request.user.phone_number,
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

    def authorize(self, request):
        ro_id = request.data['payload']['payment']['entity']['order_id']
        obj = Payment.objects.get(razorpay_order_id=ro_id)
        obj.paid_successfully = True
        order = Order.objects.get(o_id=obj.order.o_id)
        order_products = OrderProduct.objects.filter(order=order.o_id)
        for order_product in order_products:
            product = Product.objects.get(pid=order_product.product.pid)
            product.purchase_count += order_product.quantity
            product.stock_left -= order_product.quantity
            user = product.artist
            artist = Artist.objects.get(user=user)
            artist.balance += (
                order_product.quantity * product.original_price
            )
            artist.total_sales += (
                order_product.quantity * product.original_price
            )
            order_product.ordered = True
            product.save()
            order_product.save()
            artist.save()
        order.being_delivered = True
        order.ordered_date = now()
        try:
            obj.save()
            order.save()
            return True
        except:
            return False


    def post(self, request):
        if request.headers.get('X-Razorpay-Signature') is not None:
            try:
                webhook_signature = request.headers.get('X-Razorpay-Signature')
                result = client.utility.verify_webhook_signature(
                    json.dumps(request.data, separators=(',', ':')), # pass raw data
                    webhook_signature,
                    "123456testsecret" #set secret up
                )
            except Exception as e:
                return Response(status=400)

            if request.data.get('event') == "payment.authorized":    
                if self.authorize(request):
                    return Response(status=200)
                else:
                    return Response(status=400)
    
        return Response(status=200)
            

class ArtistOrderProductView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsArtist]
    parser_classes = [JSONParser]
    serializer_class = OrderProductHandOverSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self, *args, **kwargs):
        user = self.request.user.id
        order_products = OrderProduct.objects.filter(
            order__being_delivered=True,
            order__received=False,
            handed_over=False,
            product__artist=user
        )
        return order_products


class OrderProductHandOverView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemixAdmin]
    parser_classes = [JSONParser]
    serializer_class = OrderProductHandOverSerializer

    def post(self, request):
        try:
            order_product = OrderProduct.objects.get(op_id=request.data['order_product'])
            order_product.handed_over = True
            order_product.save()
            return Response({
                'status': "success",
                'details': "Successfully stored as handed over."
            }, status=200)
        except:
            return Response({
                'status': 'error',
                'detail': 'Could not update status.'
            }, status=400)


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
    permission_classes = [permissions.IsAuthenticated, IsDemixAdmin]
    parser_classes = [JSONParser]
    serializer_class = RefundOrderSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self, *args, **kwargs):
        refund_orders = Order.objects.filter(refund_requested=True,
                                      refund_granted=False)
        return refund_orders


class GrantRefundView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemixAdmin]
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


class PendingOrdersView(ListAPIView):
    # Delivery-pending orders.
    permission_classes = [permissions.IsAuthenticated, IsDemixAdmin]
    parser_classes = [JSONParser]
    serializer_class = OrderDeliverySerializer
    pagination_class = ResultSetPagination

    def get_queryset(self, *args, **kwargs):
        pending_orders = Order.objects.filter(being_delivered=True,
                                              received=False)
        return pending_orders


class DeliveryStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemixAdmin]
    parser_classes = [JSONParser]
    serializer_class = OrderDeliverySerializer

    def post(self, request):
        try:
            order = Order.objects.get(o_id=request.data['order'])
            order.received = True
            order.save()
            return Response({
                'status': "success",
                'details': "Successfully updated status to 'received'."
            }, status=200)
        except:
            return Response({
                'status': 'error',
                'detail': 'Could not update status.'
            }, status=400)


class DailyOrderView(PandasView):
    permission_classes = [permissions.IsAuthenticated, IsDemixAdmin]
    serializer_class = OrderProductExportSerializer
    renderer_classes = [PandasExcelRenderer]

    def get_queryset(self):
        today = datetime.datetime.today()
        aware_today = make_aware(today)
        orders = list(Order.objects.values_list('o_id', flat=True).filter(ordered_date__lt=aware_today))
        order_products = OrderProduct.objects.filter(order__in=[order.urn for order in orders])
        return order_products

    def get_pandas_filename(self, request, format):
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        return f"{today}-orders"
