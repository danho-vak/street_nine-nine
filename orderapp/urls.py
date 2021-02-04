from django.urls import path

from orderapp.views import OrderListView, orderCreateView, orderPaymentCheck, orderPaymentCancel, \
    orderPaymentError, OrderDetailView, UserOrderListView

app_name = 'orderapp'

urlpatterns = [
    path('', UserOrderListView.as_view(), name='orderList'),
    path('<int:pk>/complete/', OrderDetailView.as_view(), name='complete'),
    path('create/', OrderListView.as_view(), name='list'),
    path('create/new/', orderCreateView, name='createOrder'),
    path('payment/check/', orderPaymentCheck, name='paymentCheck'),
    path('payment/error/', orderPaymentError, name='paymentError'),
    path('cancel/', orderPaymentCancel, name='paymentCancel'),
]
