from rest_framework import serializers
from .models import Order, OrderProduct
from products.serializers import ProductSerializer


class ParticularOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['o_id', 'user', 'products', 'shipping_address', 'billing_address', 
                  'coupon', 'start_date', 'ordered_date', 'being_delivered',
                  'received', 'refund_requested', 'refund_granted']


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderproduct_set = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('o_id', 'user', 'shipping_address', 'billing_address', 
                  'coupon', 'start_date', 'ordered_date', 'being_delivered',
                  'received', 'refund_requested', 'refund_granted', 'orderproduct_set')

