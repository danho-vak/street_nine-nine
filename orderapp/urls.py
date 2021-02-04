from django.urls import path

from orderapp.views import OrderListView, orderCreateView, orderPaymentCheck, UserOrderListView, orderPaymentCancel, \
    orderPaymentError

app_name = 'orderapp'

urlpatterns = [
    path('', UserOrderListView.as_view(), name='orderList'),
    path('create/', OrderListView.as_view(), name='list'),
    path('create/new/', orderCreateView, name='createOrder'),
    path('payment/check/', orderPaymentCheck, name='paymentCheck'),
    path('payment/error/', orderPaymentError, name='paymentError'),
    path('cancel/', orderPaymentCancel, name='paymentCancel'),
]
