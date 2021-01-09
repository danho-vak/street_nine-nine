from django.urls import path

from productapp.views import ProductCreateView, ProductCategoryCreateView

app_name = 'productapp'

urlpatterns = [
    path('categories/create/', ProductCategoryCreateView.as_view(), name='categoryCreate'),
    path('create/', ProductCreateView.as_view(), name='infoCreate'),
]