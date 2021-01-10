from django.urls import path

from productapp.views import ProductCreateView, ProductCategoryCreateView, ProductDetailView

app_name = 'productapp'

urlpatterns = [
    path('categories/create/', ProductCategoryCreateView.as_view(), name='categoryCreate'),
    path('create/', ProductCreateView.as_view(), name='infoCreate'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
]