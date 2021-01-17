from django.urls import path

from productapp.views import ProductCreateView, ProductCategoryCreateView, ProductDetailView, ProductDeleteView, \
    ProductUpdateView, ProductImageAll, ProductImageChangeView, ProductImageDeleteView, ProductThumbnailCreateView, \
    ProductDetailImageCreateView

app_name = 'productapp'

urlpatterns = [
    path('categories/create/', ProductCategoryCreateView.as_view(), name='categoryCreate'),
    path('create/', ProductCreateView.as_view(), name='infoCreate'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('images/<int:pk>/', ProductImageAll.as_view(), name='images'),
    path('images/<int:pk>/thumbnail/create/', ProductThumbnailCreateView.as_view(), name='thumbnailCreate'),
    path('images/<int:pk>/detail/create/', ProductDetailImageCreateView.as_view(), name='detailCreate'),
    path('images/delete/<int:pk>/', ProductImageDeleteView, name='imageDelete'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('test/<int:pk>/', ProductImageChangeView, name='changeImage')  # FBV
]