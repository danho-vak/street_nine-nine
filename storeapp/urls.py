from django.urls import path

from storeapp.views import StoreMainList, StoreSearchResultView, StoreCategoryResultView

app_name = 'storeapp'

urlpatterns = [
    path('', StoreMainList.as_view(), name='index'),
    path('search/', StoreSearchResultView.as_view(), name='search'),
    path('search/<int:category_code>', StoreCategoryResultView.as_view(), name='searchByCategory'),
]