from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from accounts.models import Address
import uuid
# Create your models here.

User = get_user_model()


class Coupon(models.Model):
    code = models.CharField(max_length=15, primary_key=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return self.code


class Order(models.Model):
    o_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address,
        related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address,
        related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True, blank=True)

    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name}'s order at {self.start_date}"
    
    @property
    def get_total(self):
        total = 0
        for order_product in self.order_products.all():
            total += order_product.get_final_price
        if self.coupon:
            total  -= self.coupon.price
        return total


class OrderProduct(models.Model):
    op_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    @property
    def get_total_product_price(self):
        return self.quantity * self.product.kalafex_price

    @property
    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price

    @property
    def get_price_saved(self):
        return self.get_total_product_price - self.get_total_discount_product_price

    @property
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price
        return self.get_total_product_price

    class Meta:
        ordering = ['-date_created']


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    razorpay_order_id = models.TextField()
    razorpay_payment_id = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    paid_successfully = models.BooleanField(default=False)
    
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name}'s Razorpay Payment - {self.razorpay_order_id}"


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reasons = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.pk

