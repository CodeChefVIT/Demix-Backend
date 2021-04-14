from django.urls import path
from .views import (
    OrderCreateView,
    OrderModifyView,
    ParticularOrderView,
    OrderListView,
    PreviousOrdersListView,
    OrderProductCreateView,
    OrderProductModifyView,
    CartView,
    PaymentCreateView,
    PaymentVerifyView,
    RequestRefundView,
    RefundRequestsView,
    GrantRefundView
)

urlpatterns = [
    path('create/order/', OrderCreateView.as_view()),
    path('modify/order/<str:o_id>/', OrderModifyView.as_view()),
    path('view/orders/', OrderListView.as_view()),
    path('view/previous_orders/', PreviousOrdersListView.as_view()),
    path('view/order/<str:o_id>/', ParticularOrderView.as_view()),
    path('create/order_product/', OrderProductCreateView.as_view()),
    path('modify/order_product/<str:op_id>/', OrderProductModifyView.as_view()),
    path('view/cart/', CartView.as_view()),
    path('create/payment/', PaymentCreateView.as_view()),
    path('verify/payment/', PaymentVerifyView.as_view()),
    path('request_refund/', RequestRefundView.as_view()),
    path('view/refund_requests/', RefundRequestsView.as_view()),
    path('grant/refund/', GrantRefundView.as_view()),
]