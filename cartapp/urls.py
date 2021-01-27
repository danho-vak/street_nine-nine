from django.urls import path

from cartapp.views import CartItemCreateView, CartListView, CartItemDeleteView

app_name = 'cartapp'


urlpatterns = [
    path('', CartListView.as_view(), name='list'),
    path('add/', CartItemCreateView, name='add'),
    path('delete/<int:cart_pk>', CartItemDeleteView, name='delete'),
]
