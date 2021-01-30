from django.urls import path

from orderapp.views import OrderListView

app_name = 'orderapp'

urlpatterns = [
    path('', OrderListView.as_view(), name='list')
]