from django.urls import path

from orderapp.views import OrderListView, orderCreateView, orderPaymentCheck

app_name = 'orderapp'

urlpatterns = [
    path('create/', OrderListView.as_view(), name='list'),
    path('create/new/', orderCreateView, name='createOrder'),
    path('payment/check/', orderPaymentCheck, name='paymentCheck'),
]