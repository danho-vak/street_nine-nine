from django.urls import path

from cartapp.views import CartItemCreateView, CartListView, CartItemDeleteView, CartItemQuantityUpdateView

app_name = 'cartapp'


urlpatterns = [
    path('', CartListView.as_view(), name='list'),
    path('add/', CartItemCreateView, name='add'),
    path('delete/<int:cart_pk>', CartItemDeleteView, name='delete'),
    path('items/update/<int:cart_pk>', CartItemQuantityUpdateView, name='quantityUpdate'),
]
