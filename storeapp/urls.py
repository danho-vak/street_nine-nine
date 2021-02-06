from django.urls import path

from storeapp.views import StoreMainList, StoreSearchResultView

app_name = 'storeapp'

urlpatterns = [
    path('', StoreMainList.as_view(), name='index'),
    path('search/', StoreSearchResultView.as_view(), name='search'),
]