from django.urls import path

from productapp.views import ProductCreateView, ProductCategoryCreateView, ProductDetailView, ProductDeleteView, \
    ProductUpdateView, ProductImageAll, ProductImageChangeView, ProductImageDeleteView, ProductThumbnailCreateView, \
    ProductDetailImageCreateView

app_name = 'productapp'

urlpatterns = [
    path('categories/create/', ProductCategoryCreateView.as_view(), name='categoryCreate'),                   # 카테고리 등록
    path('create/', ProductCreateView.as_view(), name='infoCreate'),                                          # 상품 등록
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),                                     # 상품 상세페이지
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update'),                                     # 상품 정보 업데이트
    path('images/<int:pk>/', ProductImageAll.as_view(), name='images'),                                       # 상품 모든 이미지
    path('images/<int:pk>/thumbnail/create/', ProductThumbnailCreateView.as_view(), name='thumbnailCreate'),  # 상품 썸네일 업로드
    path('images/<int:pk>/detail/create/', ProductDetailImageCreateView.as_view(), name='detailCreate'),      # 상품 상세페이지 업로드
    path('images/delete/<int:pk>/', ProductImageDeleteView, name='imageDelete'),                              # 상품 이미지 삭제
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),                                     # 상품 삭제
    path('images/<int:pk>/update/', ProductImageChangeView, name='changeImage')                               # 상품 이미지 업데이트
]