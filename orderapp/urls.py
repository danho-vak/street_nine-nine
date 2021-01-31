from django.urls import path

from orderapp.views import OrderListView, OrderCreateView

app_name = 'orderapp'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='list')
]