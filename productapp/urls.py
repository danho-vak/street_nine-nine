from django.urls import path

from productapp.views import ProductCreateView, ProductCategoryCreateView

app_name = 'productapp'

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='create'),
    path('category/create/', ProductCategoryCreateView.as_view(), name='categoryCreate'),
]