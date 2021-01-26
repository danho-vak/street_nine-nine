from django.urls import path

from cartapp.views import AddCartView

app_name = 'cartapp'


urlpatterns = [
    path('add/', AddCartView, name='add'),
]
