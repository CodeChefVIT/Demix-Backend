from rest_framework import serializers
from .models import Order, OrderProduct, Payment, Refund
from products.serializers import ProductSerializer
from accounts.models import Address


class ParticularOrderSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField('_get_order_price')

    def _get_order_price(self, obj):
        price = obj.get_total()
        return price

    class Meta:
        model = Order
        fields = ['o_id', 'user', 'products', 'shipping_address', 'billing_address', 
                  'coupon', 'start_date', 'ordered_date', 'being_delivered',
                  'received', 'refund_requested', 'refund_granted', 'price']


class OrderProductCrudSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderProduct
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        optional_fields = ['razorpay_payment_id']


class RefundSerializer(serializers.ModelSerializer):

    def run_validators(self, value):
        for validator in self.validators:
            if isinstance(validator, validators.UniqueTogetherValidator):
                self.validators.remove(validator)
        super(RefundSerializer, self).run_validators(value)

    def create(self, validated_data):
        instance, _ = Refund.objects.get_or_create(**validated_data)
        return instance


    class Meta:
        model = Refund
        fields = '__all__'  


class OrderSerializer(serializers.ModelSerializer):
    orderproduct_set = OrderProductSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField('_get_order_price')
    payment = PaymentSerializer(read_only=True)
    refund = RefundSerializer(read_only=True)

    def _get_order_price(self, obj):
        price = obj.get_total
        return price

    class Meta:
        model = Order
        fields = ['o_id', 'user', 'shipping_address', 'billing_address', 
                  'coupon', 'start_date', 'ordered_date', 'being_delivered',
                  'received', 'refund_requested', 'refund_granted',
                  'orderproduct_set', 'price', 'payment', 'refund']


class OrderProductExportSerializer(serializers.ModelSerializer):
    o_id = serializers.SerializerMethodField('_get_o_id')
    name = serializers.SerializerMethodField('_get_product_name')
    shipping_address = serializers.SerializerMethodField('_get_shipping_address')
    pickup_address = serializers.SerializerMethodField('_get_pickup_address')

    def _get_o_id(self, obj):
        return obj.order.o_id

    def _get_product_name(self, obj):
        return obj.product.name
    
    def _get_shipping_address(self, obj):
        address_list = [
            str(obj.order.shipping_address.street), str(obj.order.shipping_address.city),
            str(obj.order.shipping_address.state), str(obj.order.shipping_address.pin_code)
        ]
        address_string = ", ".join(address_list)
        return address_string

    def _get_pickup_address (self, obj):
        address = Address.objects.filter(user=obj.product.artist, address_type="Pickup")[0]
        address_list = [str(address.street), str(address.city),
                        str(address.state), str(address.pin_code)]
        address_string = ", ".join(address_list)
        return address_string

    class Meta:
        model = OrderProduct
        fields = ['o_id', 'name', 'shipping_address', 'pickup_address', 'quantity']


class RefundOrderSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    refund = RefundSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['o_id', 'user', 'refund_requested', 'refund_granted',
                  'payment', 'refund']

