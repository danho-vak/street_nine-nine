from django.urls import path

from cartapp.views import CartItemCreateView

app_name = 'cartapp'


urlpatterns = [
    path('add/', CartItemCreateView, name='add'),
]
