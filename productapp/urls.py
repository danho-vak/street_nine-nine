from django.urls import path

from productapp.views import ProductCreateView

app_name = 'productapp'

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create'),
]